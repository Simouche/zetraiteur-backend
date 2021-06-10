function createExtra() {
    const url = '/extras/create/'
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: (response) => {
            const modal = $('#create-extra-modal')
            modal.find('.modal-content').html(response)
            modal.modal()
        },
        error: (jqXHR, textStatus, errorThrown) => console.log(errorThrown)
    })
}

function updateExtra(id) {
    const url = `/extras/${id}/update/`
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        success: (response) => {
            const modal = $('#create-extra-modal')
            modal.find(".modal-content").html(response)
            modal.modal()
        },
        error: (jqXHR, textStatus, errorThrown) => console.log(errorThrown)
    })
}

function deleteExtra(id) {
    const url = `/extras/${id}/delete/`
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: (response) => {
            const modal = $("#delete-extra-modal")
            modal.find(".modal-content").html(response)
            modal.modal()
        },
        error: (jqXHR, textStatus, errorThrown) => console.log(errorThrown)
    })
}

$(document).ready(function () {
    $(".info-btn").each(function () {
        $(this).on("click", () => updateExtra($(this).data('id')))
    })

    $(".delete-btn").each(function () {
        $(this).on("click", () => deleteExtra($(this).data('id')))
    })
})