
function toggleFieldsets(set1, set2, value) {
    if (value === 'SFTP') {
        set1[0].style.display = 'block'
        set2[0].style.display = 'none'
    } else {
        set1[0].style.display = 'none'
        set2[0].style.display = 'block'
    }
}

function initDynamicField()
{
    const field = document.getElementById("id_datasource_type")
    const sftp_fields = document.getElementsByClassName("sftp-config")
    const mqtt_fields = document.getElementsByClassName("mqtt-config")

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
