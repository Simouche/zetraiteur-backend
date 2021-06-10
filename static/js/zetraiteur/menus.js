function createMenu() {
    const url = '/menus/create/'
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: (response) => {
            const modal = $('#create-menu-modal')
            modal.find('.modal-content').html(response)
            modal.modal()
        },
        error: (jqXHR, textStatus, errorThrown) => console.log(errorThrown)
    })
}

function updateMenu(id) {
    const url = `/menus/${id}/update/`
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        success: (response) => {
            const modal = $('#create-menu-modal')
            modal.find(".modal-content").html(response)
            modal.modal()
        },
        error: (jqXHR, textStatus, errorThrown) => console.log(errorThrown)
    })
}

function deleteMenu(id) {
    const url = `/menus/${id}/delete/`
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: (response) => {
            const modal = $("#delete-menu-modal")
            modal.find(".modal-content").html(response)
            modal.modal()
        },
        error: (jqXHR, textStatus, errorThrown) => console.log(errorThrown)
    })
}

$(document).ready(function () {
    $(".info-btn").each(function () {
        $(this).on("click", () => updateMenu($(this).data('id')))
    })

    $(".delete-btn").each(function () {
        $(this).on("click", () => deleteMenu($(this).data('id')))
    })
})