
function toggleFieldsets(sftp_fields, mqtt_fields, parsers, value) {
    if (value === 'SFTP') {
        sftp_fields.style.display = 'block'
        parsers.style.display = 'block'
        mqtt_fields.style.display = 'none'
    } else {
        sftp_fields.style.display = 'none'
        parsers.style.display = 'none'
        mqtt_fields.style.display = 'block'
    }
}

function initDynamicField()
{
    const field = document.getElementById("id_datasource_type")

    const sftp_fields = document.getElementsByClassName("sftp-settings")[0]
    const mqtt_fields = document.getElementsByClassName("mqtt-settings")[0]
    const parsers = document.getElementById("parser_set-group")

    if(field === null) {
        return;
    }

    field.addEventListener('change', function () {
        toggleFieldsets(sftp_fields, mqtt_fields, parsers, field.value)
    })

    toggleFieldsets(sftp_fields, mqtt_fields, parsers, field.value)
}

$(document).ready(function() {
    initDynamicField();
});
