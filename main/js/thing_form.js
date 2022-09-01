
function toggleFieldsets(sets1, sets2, value) {
    if (value === 'SFTP') {
        sets1[0].style.display = 'block'
        sets2[0].style.display = 'none'
    } else {
        sets1[0].style.display = 'none'
        sets2[0].style.display = 'block'
    }
}

function initDynamicField()
{
    const field = document.getElementById("id_datasource_type")
    const sftp_fields = document.getElementsByClassName("sftp-settings")
    const mqtt_fields = document.getElementsByClassName("mqtt-settings")

    if(field === null) {
        return;
    }

    field.addEventListener('change', function () {
        toggleFieldsets(sftp_fields, mqtt_fields, field.value)
    })

    toggleFieldsets(sftp_fields, mqtt_fields, field.value)
}

$(document).ready(function() {
    initDynamicField();
});
