
function toggleFieldsets(set1, set2, value) {
    if (value === 'SFTP') {
        set1.style.display = 'block'
        set2.style.display = 'none'
    } else {
        set1.style.display = 'none'
        set2.style.display = 'block'
    }
}

function initDynamicField()
{
    const field = document.getElementById("id_type")
    const sftp_fields = document.getElementById("sftpsettings-group")
    const mqtt_fields = document.getElementById("mqttsettings-group")

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
