function clientDetails(id) {
    const url = `/clients/${id}/details/`
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        success: (response) => {
            const modal = $('#show-client-modal')
            modal.find(".modal-content").html(response)
            modal.modal()
        },
        error: (jqXHR, textStatus, errorThrown) => console.log(errorThrown)
    })
}

function deleteClient(id) {
    const url = `/clients/${id}/delete/`
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: (response) => {
            const modal = $("#delete-client-modal")
            modal.find(".modal-content").html(response)
            modal.modal()
        },
        error: (jqXHR, textStatus, errorThrown) => console.log(errorThrown)
    })
}


$(document).ready(function () {
    $(".info-btn").each(function () {
        $(this).on("click", () => clientDetails($(this).data('id')))
    })

    $(".delete-btn").each(function () {
        $(this).on("click", () => deleteClient($(this).data('id')))
    })
})