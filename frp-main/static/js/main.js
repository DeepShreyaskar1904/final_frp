console.log("✅ FIXED MAIN.JS LOADED");

(function () {
    "use strict";

    // ==================================================
    // STUDENT REVIEW FORM CONFIRMATION
    // ==================================================

    document.addEventListener("DOMContentLoaded", function () {

        const form = document.getElementById("reviewForm");

        if (form) {

            form.addEventListener("submit", function (event) {

                event.preventDefault();

                if (typeof Swal === "undefined") {
                    form.submit();
                    return;
                }

                Swal.fire({
                    title: "Submit Feedback?",
                    text: "Please make sure your feedback is honest before submitting.",
                    icon: "question",
                    showCancelButton: true,
                    confirmButtonText: "Yes, Submit",
                    cancelButtonText: "Review Again",
                    reverseButtons: true,
                    customClass: {
                        popup: "portal-swal-popup",
                        confirmButton: "portal-swal-confirm"
                    }
                }).then(function (result) {

                    if (result.isConfirmed) {
                        form.submit();
                    }

                });

            });

        }


        // ==================================================
        // ADMIN PASSWORD TOGGLE
        // ==================================================

        const togglePassword =
            document.getElementById("togglePassword");

        const passwordInput =
            document.getElementById("password");

        if (togglePassword && passwordInput) {

            togglePassword.addEventListener(
                "click",
                function () {

                    const isPassword =
                        passwordInput.getAttribute("type") === "password";

                    passwordInput.setAttribute(
                        "type",
                        isPassword ? "text" : "password"
                    );

                    const icon =
                        this.querySelector("i");

                    if (icon) {

                        if (isPassword) {

                            icon.classList.remove("fa-eye");
                            icon.classList.add("fa-eye-slash");

                            this.setAttribute(
                                "aria-label",
                                "Hide password"
                            );

                        } else {

                            icon.classList.remove("fa-eye-slash");
                            icon.classList.add("fa-eye");

                            this.setAttribute(
                                "aria-label",
                                "Show password"
                            );

                        }

                    }

                }
            );

        }


        // ==================================================
        // FULL REVIEW MODAL
        // ==================================================
        //
        // IMPORTANT:
        // No fetch()
        // No AJAX
        // No redirect
        //
        // Review information is already present inside
        // the View button using data-* attributes.
        // This is mobile-safe.
        // ==================================================

        const reviewModalElement =
            document.getElementById("reviewModal");

        if (!reviewModalElement) {
            return;
        }

        if (typeof bootstrap === "undefined") {
            console.error("❌ Bootstrap JS not loaded.");
            return;
        }

        const reviewModal =
            new bootstrap.Modal(reviewModalElement);


        // ==================================================
        // FIND ALL VIEW BUTTONS
        // ==================================================

        document
            .querySelectorAll(".view-review-btn")
            .forEach(function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        console.log(
                            "Opening review:",
                            this.getAttribute("data-review-id")
                        );


                        // ==========================================
                        // READ DATA FROM BUTTON
                        // ==========================================

                        const studentName =
                            this.getAttribute("data-student-name") || "N/A";

                        const studentEmail =
                            this.getAttribute("data-student-email") || "N/A";

                        const course =
                            this.getAttribute("data-course") || "N/A";

                        const batch =
                            this.getAttribute("data-batch") || "N/A";

                        const rating =
                            this.getAttribute("data-rating") || "0";

                        const teaching =
                            this.getAttribute("data-teaching") || "0";

                        const communication =
                            this.getAttribute("data-communication") || "0";

                        const practical =
                            this.getAttribute("data-practical") || "0";

                        const doubt =
                            this.getAttribute("data-doubt") || "0";

                        const sentiment =
                            this.getAttribute("data-sentiment") || "neutral";

                        const feedback =
                            this.getAttribute("data-feedback") ||
                            "No feedback provided.";

                        const createdAt =
                            this.getAttribute("data-created-at") || "N/A";


                        // ==========================================
                        // STUDENT INFORMATION
                        // ==========================================

                        const studentNameElement =
                            document.getElementById("detailStudentName");

                        const studentEmailElement =
                            document.getElementById("detailStudentEmail");

                        const courseElement =
                            document.getElementById("detailCourse");

                        const batchElement =
                            document.getElementById("detailBatch");


                        if (studentNameElement) {
                            studentNameElement.textContent = studentName;
                        }

                        if (studentEmailElement) {
                            studentEmailElement.textContent = studentEmail;
                        }

                        if (courseElement) {
                            courseElement.textContent = course;
                        }

                        if (batchElement) {
                            batchElement.textContent = batch;
                        }


                        // ==========================================
                        // RATINGS
                        // ==========================================

                        const ratingElement =
                            document.getElementById("detailRating");

                        const teachingElement =
                            document.getElementById("detailTeaching");

                        const communicationElement =
                            document.getElementById("detailCommunication");

                        const practicalElement =
                            document.getElementById("detailPractical");

                        const doubtElement =
                            document.getElementById("detailDoubt");


                        if (ratingElement) {
                            ratingElement.textContent =
                                `${rating}/5 ⭐`;
                        }

                        if (teachingElement) {
                            teachingElement.textContent =
                                `${teaching}/5 ⭐`;
                        }

                        if (communicationElement) {
                            communicationElement.textContent =
                                `${communication}/5 ⭐`;
                        }

                        if (practicalElement) {
                            practicalElement.textContent =
                                `${practical}/5 ⭐`;
                        }

                        if (doubtElement) {
                            doubtElement.textContent =
                                `${doubt}/5 ⭐`;
                        }


                        // ==========================================
                        // SENTIMENT
                        // ==========================================

                        const sentimentElement =
                            document.getElementById("detailSentiment");

                        const formattedSentiment =
                            sentiment.charAt(0).toUpperCase() +
                            sentiment.slice(1);


                        if (sentimentElement) {
                            sentimentElement.textContent =
                                formattedSentiment;
                        }


                        // ==========================================
                        // FEEDBACK
                        // ==========================================

                        const feedbackElement =
                            document.getElementById("detailFeedback");


                        if (feedbackElement) {
                            feedbackElement.textContent = feedback;
                        }


                        // ==========================================
                        // DATE
                        // ==========================================

                        const createdAtElement =
                            document.getElementById("detailCreatedAt");


                        if (createdAtElement) {
                            createdAtElement.textContent =
                                createdAt;
                        }


                        // ==========================================
                        // OPEN MODAL
                        // ==========================================

                        reviewModal.show();

                    }
                );

            });

    });

})();