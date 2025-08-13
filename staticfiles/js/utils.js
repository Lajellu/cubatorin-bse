function truncateString(str, num) {
    if (str.length > num) {
        return str.slice(0, num) + "..."
    } else {
        return str
    }
}

function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";")
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim()
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                )
                break
            }
        }
    }
    return cookieValue
}

function setupAutosave(tableName) {
    console.log("setupAutosave")
    $("input, textarea, select").on("blur", function () {
        console.log("unfocused")

        const fieldName = $(this).attr("data-db-field")
        const fieldValue = $(this).val()

        console.log("Unfocused field:", fieldName)
        console.log("Value:", fieldValue)

        // Optional: Make sure required info exists
        if (!fieldName || !teamId) {
            console.warn("Missing 'name' or 'data-team-id' on field.")
            return
        }

        const headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        }

        // Post to your Django API
        $.ajax({
            url: "/api/save_field/",
            method: "POST",
            headers: headers,
            contentType: "application/json",
            data: JSON.stringify({
                table: tableName,
                field: fieldName,
                value: fieldValue,
                team_id: teamId,
            }),
            success: function (response) {
                console.log("Saved successfully:", response)
            },
            error: function (xhr, status, error) {
                console.error("Error saving field:", xhr.responseText || error)
            },
        })
    })
}
