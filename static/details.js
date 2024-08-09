$(document).ready(function(){
    $('#getInfoBtn').on('click', function(){
        let regno = $('#regno').val();
        $.ajax({
            url: '/details',
            method: 'POST',
            data: { regno: regno },
            success: function(response) {
                if (response.student) {
                    $('#rollNo').text(response.student.roll_no);
                    $('#name').text(response.student.name);
                    $('#company').text(response.student.company);
                    $('#campusStatus').text(response.student.campus_status);
                    $('#batch').text(response.student.batch);
                    if (response.student.campus_status=== 'HIGHER EDUCATION') {
                        $('#companyLabel').text('University:');
                    } else {
                        $('#companyLabel').text('Company Employed:');
                    }
                    $('#studentDetails').show();
                    $('#errorMessage').text('');
                } else if (response.error) {
                    $('#errorMessage').text(response.error);
                    $('#studentDetails').hide();
                }
            }
        });
    });
});
