function createFood() {
    const url = '/foods/create/'
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: (response) => {
            const modal = $('#create-food-modal')
            modal.find('.modal-content').html(response)
            modal.modal()
        },
        error: (jqXHR, textStatus, errorThrown) => console.log(errorThrown)
    })
}

function updateFood(id) {
    const url = `/foods/${id}/update/`
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        success: (response) => {
            const modal = $('#create-food-modal')
            modal.find(".modal-content").html(response)
            modal.modal()
        },
        error: (jqXHR, textStatus, errorThrown) => console.log(errorThrown)
    })
}

function deleteFood(id) {
    const url = `/foods/${id}/delete/`
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: (response) => {
            const modal = $("#delete-food-modal")
            modal.find(".modal-content").html(response)
            modal.modal()
        },
        error: (jqXHR, textStatus, errorThrown) => console.log(errorThrown)
    })
}

$(document).ready(function () {
    $(".info-btn").each(function () {
        $(this).on("click", () => updateFood($(this).data('id')))
    })

    $(".delete-btn").each(function () {
        $(this).on("click", () => deleteFood($(this).data('id')))
    })
})