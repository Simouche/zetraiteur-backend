function orderDetails(id) {
    window.location.href = `/orders/${id}/details/`
}

$(document).ready(function () {
    $(".info-btn").each(function () {
        $(this).on("click", () => orderDetails($(this).data('id')))
    })
})