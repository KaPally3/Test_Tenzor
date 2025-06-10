#!/bin/bash

units=$(systemctl list-units --type=service --no-legend | awk '{print $1}' | grep '^foobar-.*\.service$')

for unit in $units; do
    service_name=$(echo "$unit" | sed -E 's/^foobar-(.*)\.service$/\1/')

    start_path="/opt/misc/$service_name"
    end_path="/srv/data/$service_name"
    unit_file=$(systemctl show -p FragmentPath "$unit" | cut -d= -f2)

    systemctl stop "$unit"

    mkdir -p "$(dirname "$end_path")"
    mv "$start_path" "$end_path"

    temp_unit=$(mktemp)
    sed -E \
        -e "s|^WorkingDirectory=/opt/misc/$service_name|WorkingDirectory=/srv/data/$service_name|" \
        -e "s|^ExecStart=/opt/misc/$service_name/foobar-daemon\b|ExecStart=/srv/data/$service_name/foobar-daemon|" \
        "$unit_file" > "$temp_unit"

    mv "$temp_unit" "$unit_file"

    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl start "$unit"
done
