/*
 * Builds the date picker. Assigns listeners to each textfield
 */

$(function () {
    var dateFormat = "mm/dd/yy",
        from = $("#from")
            .datepicker({
                defaultDate: new Date(min_date),
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
                minDate: new Date(min_date),
                maxDate: new Date(max_date)
            })
            .datepicker("setDate", new Date(min_date))
            .on("change", function () {
                to.datepicker("option", "minDate", getDate(this));
            }),
        to = $("#to").datepicker({
            defaultDate: new Date(max_date),
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            minDate: new Date(min_date),
            maxDate: new Date(max_date),
        })
        .datepicker("setDate", new Date(max_date))
        .on("change", function () {
            from.datepicker("option", "maxDate", getDate(this));
        });

    function getDate(element) {
        var date;
        try {
            date = $.datepicker.parseDate(dateFormat, element.value);
        } catch (error) {
            date = null;
        }

        return date;
    }
});