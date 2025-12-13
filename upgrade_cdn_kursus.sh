#!/bin/bash

################################################################################
# Upgrade Module Odoo - Docker
# -------------------------------------------------------------------------------
# 📌 Wajib chmod +x terlebih dahulu sebelum dijalankan
# Contoh: sudo chmod +x upgrade_cdn_base.sh
#
# 📌 Contoh Perintah:
#   ./upgrade_cdn_kursus.sh                              # Default DB, module, container
#   ./upgrade_cdn_kursus.sh -d db_test                   # Pakai db_test
#   ./upgrade_cdn_kursus.sh -u modul_baru                # Pakai modul_baru
#   ./upgrade_cdn_kursus.sh -d db_test -u modul_baru     # Pakai db_test + modul_baru
#   ./upgrade_cdn_kursus.sh -c container_name            # Ganti container
#   ./upgrade_cdn_kursus.sh -d db_test -u modul_baru -c odoo_custom
################################################################################

# Default values (ubah sesuai kebutuhan)
DB_NAME="db_kursus"
MODULE_NAME="kursus"
ODOO_CONTAINER="odoo-18-docker-odoo18-1"
DB_HOST="db"
DB_USER="odoo"
DB_PASSWORD="odoo18@2024"

# Fungsi bantuan penggunaan script
usage() {
  echo "===================================================="
  echo "Usage: $0 [-d <datakursus_name>] [-u <module_name>] [-c <container_name>]"
  echo ""
  echo "Contoh:"
  echo "  $0                                  -> default semua"
  echo "  $0 -d db_test                       -> update module default di db_test"
  echo "  $0 -u modul_baru                    -> update modul_baru di default DB"
  echo "  $0 -d db_test -u modul_baru         -> tentukan DB & Modul"
  echo "  $0 -d db_test -u modul_baru -c odoo_custom -> ganti container"
  echo "===================================================="
  exit 1
}

# Parsing parameter -d (datakursus), -u (module), -c (container)
while getopts "d:u:c:h" opt; do
  case "$opt" in
    d) DB_NAME="$OPTARG" ;;
    u) MODULE_NAME="$OPTARG" ;;
    c) ODOO_CONTAINER="$OPTARG" ;;
    h) usage ;;
    *) usage ;;
  esac
done

# Informasi sebelum eksekusi
echo "===================================================="
echo "🔧 Starting Module Update"
echo "Datakursus   : $DB_NAME"
echo "Module     : $MODULE_NAME"
echo "Container  : $ODOO_CONTAINER"
echo "===================================================="

# Eksekusi update modul di Docker container
docker exec -it "$ODOO_CONTAINER" odoo \
  -d "$DB_NAME" \
  -u "$MODULE_NAME" \
  --db_host="$DB_HOST" \
  --db_user="$DB_USER" \
  --db_password="$DB_PASSWORD" \
  --stop-after-init

# Status selesai
if [ $? -eq 0 ]; then
  echo "✅ Update completed successfully."
else
  echo "❌ Update failed. Periksa log untuk detail lebih lanjut."
fi
