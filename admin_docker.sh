#!/bin/bash
# =============================================================================
# admin_docker.sh — Script d'administration de pep-web (Car Horizon) woohoo yay 
# Projet SAE — Déploiement d'infrastructure réseau et web
# Stack : Flask (Python 3.10) + MySQL 8.0, orchestrée via docker-compose
# Version : 2.0
# Usage   : ./admin_docker.sh [start|stop|restart|status|update|logs|--fun]
# =============================================================================

# -----------------------------------------------------------------------------
# CONFIGURATION — Modifier ces variables selon l'environnement de déploiement
# -----------------------------------------------------------------------------
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"  # Répertoire du projet (où se trouve docker-compose.yml)
COMPOSE_FILE="${PROJECT_DIR}/docker-compose.yml"

# Noms des services tels que définis dans docker-compose.yml
SERVICE_WEB="web"                       # Service Flask 
SERVICE_DB="db"                         # Service MySQL

# Noms des conteneurs générés par docker-compose (format: <dossier>_<service>_1)
# Note : docker-compose préfixe avec le nom du dossier parent en minuscules
CONTAINER_WEB="pep-web-web-1"
CONTAINER_DB="pep-web-db-1"

# Réseau et accès
SERVER_IP="192.168.32.50"              
SERVER_PORT="80"                      # Port Flask exposé

# Couleurs ANSI pour le terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# -----------------------------------------------------------------------------
# FONCTIONS UTILITAIRES
# -----------------------------------------------------------------------------

info()    { echo -e "${CYAN}[INFO]${RESET}  $1"; }
success() { echo -e "${GREEN}[OK]${RESET}    $1"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET}  $1"; }
error()   { echo -e "${RED}[ERREUR]${RESET} $1" >&2; exit 1; }

# On vérifie que docker et docker-compose sont disponibles sur le système
check_deps() {
    if ! command -v docker &>/dev/null; then
        error "Docker n'est pas installé. Lance : sudo apt install docker.io"
    fi
    # Supporte docker compose (v2, plugin) ET docker-compose (v1, binaire standalone)
    if docker compose version &>/dev/null 2>&1; then
        COMPOSE_CMD="docker compose"
    elif command -v docker-compose &>/dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        error "docker compose introuvable. Lance : sudo apt install docker-compose-plugin"
    fi
}

# On vérifie que le fichier docker-compose.yml existe dans le répertoire du script
check_compose_file() {
    if [ ! -f "${COMPOSE_FILE}" ]; then
        error "Fichier docker-compose.yml introuvable dans : ${PROJECT_DIR}"
    fi
}

# Retourne vrai (0) si le conteneur web Flask est en cours d'exécution
web_running() {
    docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_WEB}$"
}

# Retourne vrai (0) si le conteneur MySQL est en cours d'exécution
db_running() {
    docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_DB}$"
}

# -----------------------------------------------------------------------------
# ACTIONS PRINCIPALES
# -----------------------------------------------------------------------------

# Démarre l'ensemble de la stack (web + db) avec docker-compose.
# L'option -d (detach) lance les conteneurs en arrière-plan.
# docker-compose gère automatiquement l'ordre de démarrage (db avant web)
# grâce à la directive depends_on dans le fichier de configuration.
cmd_start() {
    info "Démarrage de la stack Car Horizon (web + db)..."
    check_compose_file

    if web_running; then
        warn "La stack est déjà en cours d'exécution."
        return
    fi

    # --build force la reconstruction de l'image si des fichiers ont changé
    $COMPOSE_CMD -f "${COMPOSE_FILE}" up -d \
        && success "Stack démarrée ! Car Horizon accessible sur http://${SERVER_IP}:${SERVER_PORT}" \
        || error "Échec du démarrage de la stack."
}

# Arrête proprement tous les services de la stack.
# 'down' arrête les conteneurs ET supprime les réseaux créés,
# mais préserve le volume mysql_data (les données de la BDD sont conservées).
cmd_stop() {
    info "Arrêt de la stack Car Horizon..."
    check_compose_file

    if ! web_running && ! db_running; then
        warn "Aucun service n'est en cours d'exécution."
        return
    fi

    $COMPOSE_CMD -f "${COMPOSE_FILE}" down \
        && success "Stack arrêtée proprement. Les données MySQL sont préservées." \
        || error "Échec de l'arrêt."
}

# Redémarre tous les services sans supprimer les conteneurs ni les volumes.
# Utile pour appliquer des changements mineurs sans reconstruire les images.
cmd_restart() {
    info "Redémarrage de la stack Car Horizon..."
    check_compose_file

    $COMPOSE_CMD -f "${COMPOSE_FILE}" restart \
        && success "Stack redémarrée avec succès." \
        || error "Échec du redémarrage."
}

# Affiche l'état détaillé de chaque service de la stack.
cmd_status() {
    echo -e "\n${BOLD}=== État de la stack Car Horizon ===${RESET}\n"
    check_compose_file

    # Affiche le tableau de statut natif de docker-compose
    $COMPOSE_CMD -f "${COMPOSE_FILE}" ps
    echo ""

    # Résumé visuel coloré des deux services critiques
    if web_running; then
        success "Flask (web)  : EN COURS  → http://${SERVER_IP}:${SERVER_PORT}"
    else
        echo -e "${RED}[DOWN]${RESET}  Flask (web)  : ARRÊTÉ"
    fi

    if db_running; then
        success "MySQL  (db)  : EN COURS  → port interne 3306 (exposé: 33066)"
    else
        echo -e "${RED}[DOWN]${RESET}  MySQL  (db)  : ARRÊTÉ"
    fi
    echo ""
}

# Met à jour la stack en reconstruisant l'image web depuis le Dockerfile.
# Utile après une modification du code source ou des dépendances Python.
# Les données MySQL dans le volume nommé (mysql_data) sont préservées.
cmd_update() {
    info "Mise à jour de la stack Car Horizon..."
    check_compose_file

    info "Arrêt des services actuels..."
    $COMPOSE_CMD -f "${COMPOSE_FILE}" down || error "Impossible d'arrêter les services."

    info "Reconstruction de l'image Flask depuis le Dockerfile..."
    # --no-cache force une reconstruction complète sans utiliser le cache Docker
    $COMPOSE_CMD -f "${COMPOSE_FILE}" build --no-cache web \
        || error "Échec de la reconstruction de l'image."

    info "Redémarrage de la stack avec la nouvelle image..."
    $COMPOSE_CMD -f "${COMPOSE_FILE}" up -d \
        && success "Mise à jour terminée ! Car Horizon est de nouveau en ligne." \
        || error "Échec du redémarrage après mise à jour."
}

# Affiche les logs en temps réel des deux services.
# Très utile pour diagnostiquer les erreurs Flask ou les échecs de connexion MySQL.
# L'option --tail limite l'affichage aux N dernières lignes (évite le flood).
# Ctrl+C pour quitter le suivi en direct.
cmd_logs() {
    info "Logs en direct (Ctrl+C pour quitter)..."
    check_compose_file
    $COMPOSE_CMD -f "${COMPOSE_FILE}" logs -f --tail=50
}

# -----------------------------------------------------------------------------
# EASTER EGG — Option --fun
# Affiche un récap stylisé du projet et teste la connectivité de l'appli web.
# -----------------------------------------------------------------------------
cmd_fun() {
    echo ""
    echo -e "${CYAN}${BOLD}"
    echo "  ╔══════════════════════════════════════════════════════╗"
    echo "  ║      Car Horizon — Panneau de contrôle SAE           ║"
    echo "  ║                                                      ║"
    echo "  ║   Stack    : Flask 3.10 + MySQL 8.0                  ║"
    echo "  ╚══════════════════════════════════════════════════════╝"
    echo -e "${RESET}"

    # Test de l'endpoint principal de l'application Flask
    info "Test de l'endpoint Flask : http://${SERVER_IP}:${SERVER_PORT} ..."
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 \
                "http://${SERVER_IP}:${SERVER_PORT}" 2>/dev/null)

    case "$HTTP_CODE" in
        200) success "Page d'accueil répond ! Code HTTP : ${GREEN}200 OK${RESET} " ;;
        302) success "Redirection détectée (302) — le serveur fonctionne " ;;
        000) warn "Serveur injoignable — vérifie que la stack est démarrée (./admin_docker.sh start)" ;;
        *)   warn "Code HTTP inattendu : ${YELLOW}${HTTP_CODE}${RESET} — consulte les logs." ;;
    esac

    # Test de l'endpoint /monitoring s'il répond (page de monitoring Flask)
    echo ""
    info "Test de la page de monitoring : http://${SERVER_IP}:${SERVER_PORT}/monitoring ..."
    MON_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 \
               "http://${SERVER_IP}:${SERVER_PORT}/monitoring" 2>/dev/null)
    case "$MON_CODE" in
        200) success "Page monitoring accessible ! Code HTTP : ${GREEN}200 OK${RESET} " ;;
        302) info "Redirection (302) — probablement une page nécessitant une authentification." ;;
        000) warn "Monitoring injoignable." ;;
        *)   warn "Code HTTP monitoring : ${YELLOW}${MON_CODE}${RESET}" ;;
    esac

    echo ""
    echo -e "  ${BOLD}Raccourcis utiles :${RESET}"
    echo -e "  ${CYAN}./admin_docker.sh logs${RESET}    → logs Flask en direct"
    echo -e "  ${CYAN}./admin_docker.sh status${RESET}  → état des conteneurs"
    echo ""
}

# -----------------------------------------------------------------------------
# AIDE — Affichée si aucun argument ou argument inconnu
# -----------------------------------------------------------------------------
cmd_help() {
    echo ""
    echo -e "${BOLD}Usage :${RESET} $0 [COMMANDE]"
    echo ""
    echo -e "${BOLD}Commandes :${RESET}"
    echo -e "  ${GREEN}start${RESET}     Démarrer la stack Flask + MySQL"
    echo -e "  ${RED}stop${RESET}      Arrêter la stack (données MySQL préservées)"
    echo -e "  ${YELLOW}restart${RESET}   Redémarrer sans reconstruire les images"
    echo -e "  ${CYAN}status${RESET}    État détaillé des conteneurs"
    echo -e "  ${CYAN}update${RESET}    Reconstruire l'image web et relancer"
    echo -e "  ${CYAN}logs${RESET}      Logs en temps réel (Ctrl+C pour quitter)"
    echo -e "  ${CYAN}--fun${RESET}     Test de connectivité stylisé "
    echo ""
    echo -e "${BOLD}Stack :${RESET} ${SERVICE_WEB} (Flask:5000) + ${SERVICE_DB} (MySQL:3306)"
    echo -e "${BOLD}IP web :${RESET} http://${SERVER_IP}:${SERVER_PORT}"
    echo ""
}

# -----------------------------------------------------------------------------
# POINT D'ENTRÉE
# -----------------------------------------------------------------------------

# Vérification des dépendances au démarrage (Docker + Compose)
check_deps

case "$1" in
    start)   cmd_start   ;;
    stop)    cmd_stop    ;;
    restart) cmd_restart ;;
    status)  cmd_status  ;;
    update)  cmd_update  ;;
    logs)    cmd_logs    ;;
    --fun)   cmd_fun     ;;
    *)       cmd_help    ;;
esac

# Le script doit être placé à la RACINE du projet (à côté du docker-compose.yml)
cp admin_docker.sh ~/pep-web/
chmod +x ~/pep-web/admin_docker.sh
cd ~/pep-web
./admin_docker.sh start
