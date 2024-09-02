  $(document).ready(function() {
            // Function to show content based on clicked link
            function showContent(targetId) {
                $('.content-section').hide(); // Hide all content sections
                $(targetId).show(); // Show the target content section
            }

            // Event handler for navigation links
            $('.nav-item-one').on('click', function(e) {
                e.preventDefault(); // Prevent default link behavior

                // Get the target content section ID from the data attribute
                var targetId = $(this).data('target');

                showContent(targetId);
            });

            // Optional: Trigger the first content to show by default
            $('.nav-item-one').first().trigger('click');
        });