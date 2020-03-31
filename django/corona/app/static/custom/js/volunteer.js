
var country_list = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Anguilla", "Antigua &amp; Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia &amp; Herzegovina", "Botswana", "Brazil", "British Virgin Islands", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Cape Verde", "Cayman Islands", "Chad", "Chile", "China", "Colombia", "Congo", "Cook Islands", "Costa Rica", "Cote D Ivoire", "Croatia", "Cruise Ship", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Estonia", "Ethiopia", "Falkland Islands", "Faroe Islands", "Fiji", "Finland", "France", "French Polynesia", "French West Indies", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea Bissau", "Guyana", "Haiti", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Isle of Man", "Israel", "Italy", "Jamaica", "Japan", "Jersey", "Jordan", "Kazakhstan", "Kenya", "Kuwait", "Kyrgyz Republic", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Mauritania", "Mauritius", "Mexico", "Moldova", "Monaco", "Mongolia", "Montenegro", "Montserrat", "Morocco", "Mozambique", "Namibia", "Nepal", "Netherlands", "Netherlands Antilles", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Norway", "Oman", "Pakistan", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romania", "Russia", "Rwanda", "Saint Pierre &amp; Miquelon", "Samoa", "San Marino", "Satellite", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "South Africa", "South Korea", "Spain", "Sri Lanka", "St Kitts &amp; Nevis", "St Lucia", "St Vincent", "St. Lucia", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor L'Este", "Togo", "Tonga", "Trinidad &amp; Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks &amp; Caicos", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States Of America", "Uruguay", "Uzbekistan", "Venezuela", "Vietnam", "Virgin Islands (US)", "Yemen", "Zambia", "Zimbabwe"];
var geocoder = new google.maps.Geocoder();

$(document).ready(function () {

    var sel = document.getElementById('id_countryselet')
    for (i = 0; i < country_list.length; i++) {
        var op = document.createElement('option')
        op.value = country_list[i]
        op.innerHTML = country_list[i]
        sel.appendChild(op)
    }
    hideStuff('div_id_x')
    hideStuff('div_id_y')
    hideStuff('div_id_servicescanprovide')
    hideStuff('div_id_country')
})

function hideStuff(id) {
    document.getElementById(id).style.display = 'none'
}
function creatvol() {
    var input = document.getElementById('id_postal_code').value
    $.getJSON('http://localhost:8080/geoserver/corona/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=corona%3ACentroids&CQL_FILTER="zcta5ce10"=' + input + '&maxFeatures=50&outputFormat=application%2Fjson', function (data) {
        if (data.features.length == 0) {
            Swal.fire({
                position: 'top-end',
                icon: 'error',
                title: 'Invalid Pincode',
                showConfirmButton: false,
                timer: 1500
            })
            document.getElementById('id_postal_code').value = ''
        } else {
            var services = $('#id_servicescanprovideselect').val().join(',')
            if (services == '') {
                Swal.fire({
                    position: 'top-end',
                    icon: 'error',
                    title: 'Please select Service',
                    showConfirmButton: false,
                    timer: 1500
                })
            } else {
                $('#id_servicescanprovide').val(services)
                var country = $('#id_countryselet').val()
                if (country == '') {
                    Swal.fire({
                        position: 'top-end',
                        icon: 'error',
                        title: 'Please select Service',
                        showConfirmButton: false,
                        timer: 1500
                    })
                } else {
                    $('#id_country').val(country)
                    codeAddress(document.getElementById('id_address').value)
                }
            }
        }
    })
}



function codeAddress(address) {
    geocoder.geocode({ address: address }, function (results, status) {
        if (status == "OK") {
            //center the map over the result
            //place a marker at the location

            document.getElementById('id_x').value = results[0].geometry.location["lng"]()
            document.getElementById('id_y').value = results[0].geometry.location["lat"]()
            document.getElementById('volunteerForm').submit()
        } else if (status == "ZERO_RESULTS") {
            Swal.fire({
                position: 'top-end',
                icon: 'error',
                title: 'Enter different address',
                showConfirmButton: false,
                timer: 1500
            })
        }
    });
}