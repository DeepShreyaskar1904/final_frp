
from pathlib import Path
import base64
import requests

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# EMAIL BACKGROUND IMAGE
# =========================================================

EMAIL_BACKGROUND_PATH = (
    BASE_DIR
    / "static"
    / "images"
    / "email_background.png"
)


# =========================================================
# GMAIL API EMAIL SENDER
# =========================================================

def send_via_gmail_api(email_message):
    """
    Send an already-built Django email through Gmail API.
    """

    refresh_token = getattr(
        settings,
        "GMAIL_REFRESH_TOKEN",
        ""
    ).strip()

    if not refresh_token:
        raise RuntimeError(
            "GMAIL_REFRESH_TOKEN is not configured in environment variables."
        )

    token_response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        timeout=20,
    )

    if not token_response.ok:
        raise RuntimeError(
            "Gmail access token request failed: "
            + token_response.text
        )

    token_data = token_response.json()

    access_token = token_data.get(
        "access_token"
    )

    if not access_token:
        raise RuntimeError(
            "Gmail access token was not returned."
        )

    # Convert Django email into MIME
    mime_message = email_message.message()

    raw_message = base64.urlsafe_b64encode(
        mime_message.as_bytes()
    ).decode("utf-8").rstrip("=")

    # Send through Gmail API
    gmail_response = requests.post(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json={
            "raw": raw_message
        },
        timeout=20,
    )

    if not gmail_response.ok:
        raise RuntimeError(
            "Gmail API email send failed: "
            + gmail_response.text
        )

    print(
        "✅ Email sent successfully through Gmail API"
    )


# =========================================================
# COMMON EMAIL HTML DESIGN
# =========================================================

def build_background_email_html(
    background_url,
    title,
    message,
    description,
    button_text,
    button_url=None,
):
    """
    Common email design used for:

    1. Student thank-you email
    2. Admin notification email

    IMPORTANT:
    No image is attached to the email.
    The background image is loaded from the website URL.
    This prevents the 'noname' attachment in Gmail.
    """

    # -----------------------------------------------------
    # BUTTON
    # -----------------------------------------------------

    if button_url:

        button_html = f"""
        <table
            cellpadding="0"
            cellspacing="0"
            border="0"
            align="center"
            style="
                margin:0 auto 28px auto;
            "
        >
            <tr>

                <td
                    align="center"
                    bgcolor="#2563eb"
                    style="
                        background:#2563eb;
                        border-radius:9px;
                    "
                >

                    <a
                        href="{button_url}"
                        target="_blank"
                        style="
                            display:inline-block;
                            padding:15px 28px;

                            font-family:
                                Arial,
                                Helvetica,
                                sans-serif;

                            font-size:16px;
                            line-height:20px;

                            font-weight:700;

                            color:#ffffff;

                            text-decoration:none;

                            border-radius:9px;

                            background:#2563eb;
                        "
                    >
                        {button_text}
                    </a>

                </td>

            </tr>
        </table>
        """

    else:

        button_html = f"""
        <table
            cellpadding="0"
            cellspacing="0"
            border="0"
            align="center"
            style="
                margin:0 auto 28px auto;
            "
        >
            <tr>

                <td
                    align="center"
                    bgcolor="#2563eb"
                    style="
                        background:#2563eb;
                        border-radius:9px;
                    "
                >

                    <span
                        style="
                            display:inline-block;
                            padding:15px 28px;

                            font-family:
                                Arial,
                                Helvetica,
                                sans-serif;

                            font-size:16px;
                            line-height:20px;

                            font-weight:700;

                            color:#ffffff;

                            border-radius:9px;

                            background:#2563eb;
                        "
                    >
                        {button_text}
                    </span>

                </td>

            </tr>
        </table>
        """

    # -----------------------------------------------------
    # COMPLETE EMAIL
    # -----------------------------------------------------

    return f"""
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        {title}
    </title>

</head>


<body
    style="
        margin:0;
        padding:0;

        background:#eef3f8;

        font-family:
            Arial,
            Helvetica,
            sans-serif;
    "
>


<!-- ===================================================== -->
<!-- OUTER EMAIL CONTAINER -->
<!-- ===================================================== -->

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"

    style="
        width:100%;
        margin:0;
        padding:35px 15px;

        background:#eef3f8;
    "
>

    <tr>

        <td align="center">


            <!-- ============================================= -->
            <!-- MAIN CARD -->
            <!-- ============================================= -->

            <table
                width="600"
                height="560"
                cellpadding="0"
                cellspacing="0"
                border="0"
                align="center"

                style="
                    width:600px;
                    max-width:600px;
                    height:560px;

                    margin:0 auto;

                    background:#ffffff;

                    border-radius:22px;

                    overflow:hidden;
                "
            >

                <tr>

                    <td
                        valign="middle"
                        align="center"

                        style="
                            width:600px;
                            max-width:600px;

                            background-color:#f4f7fb;

                            background-image:
                                url('{background_url}');

                            background-repeat:
                                no-repeat;

                            background-position:
                                center;

                            background-size:
                                cover;

                            padding:
                                55px 35px;
                        "
                    >


                        <!-- ================================= -->
                        <!-- INNER WHITE CARD -->
                        <!-- ================================= -->

                        <table
                            width="530"
                            height="430"
                            cellpadding="0"
                            cellspacing="0"
                            border="0"
                            align="center"

                            style="
                                width:530px;
                                max-width:530px;
                                height:430px;

                                margin:0 auto;

                                background:#ffffff;

                                border-radius:18px;
                            "
                        >

                            <tr>

                                <td
                                    align="center"
                                    valign="middle"
                                    height="430"

                                    style="
                                        height:430px;
                                        padding:
                                            42px
                                            38px
                                            38px
                                            38px;

                                        font-family:
                                            Arial,
                                            Helvetica,
                                            sans-serif;

                                        color:#172554;

                                        text-align:center;
                                    "
                                >


                                    <!-- ========================= -->
                                    <!-- TITLE -->
                                    <!-- ========================= -->

                                    <h1
                                        style="
                                            margin:0;
                                            padding:0;

                                            font-family:
                                                Arial,
                                                Helvetica,
                                                sans-serif;

                                            font-size:30px;

                                            line-height:38px;

                                            font-weight:700;

                                            color:#172554;

                                            text-align:center;
                                        "
                                    >
                                        {title}
                                    </h1>


                                    <!-- ========================= -->
                                    <!-- BLUE LINE -->
                                    <!-- ========================= -->

                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        border="0"
                                        align="center"

                                        style="
                                            margin:
                                                16px
                                                auto
                                                24px
                                                auto;
                                        "
                                    >

                                        <tr>

                                            <td
                                                width="65"
                                                height="5"

                                                style="
                                                    width:65px;

                                                    height:5px;

                                                    background:
                                                        #2563eb;

                                                    border-radius:5px;

                                                    font-size:0;

                                                    line-height:0;
                                                "
                                            >
                                                &nbsp;
                                            </td>

                                        </tr>

                                    </table>


                                    <!-- ========================= -->
                                    <!-- MAIN MESSAGE -->
                                    <!-- ========================= -->

                                    <p
                                        style="
                                            margin:
                                                0
                                                0
                                                22px
                                                0;

                                            padding:0;

                                            font-family:
                                                Arial,
                                                Helvetica,
                                                sans-serif;

                                            font-size:19px;

                                            line-height:30px;

                                            font-weight:700;

                                            color:#1e293b;

                                            text-align:center;
                                        "
                                    >
                                        {message}
                                    </p>


                                    <!-- ========================= -->
                                    <!-- DESCRIPTION -->
                                    <!-- ========================= -->

                                    <p
                                        style="
                                            margin:
                                                0
                                                0
                                                30px
                                                0;

                                            padding:0;

                                            font-family:
                                                Arial,
                                                Helvetica,
                                                sans-serif;

                                            font-size:16px;

                                            line-height:27px;

                                            color:#64748b;

                                            text-align:center;
                                        "
                                    >
                                        {description}
                                    </p>


                                    <!-- ========================= -->
                                    <!-- BUTTON -->
                                    <!-- ========================= -->

                                    {button_html}


                                    <!-- ========================= -->
                                    <!-- FOOTER -->
                                    <!-- ========================= -->

                                    <p
                                        style="
                                            margin:0;
                                            padding:0;

                                            font-family:
                                                Arial,
                                                Helvetica,
                                                sans-serif;

                                            font-size:13px;

                                            line-height:20px;

                                            color:#94a3b8;

                                            text-align:center;
                                        "
                                    >
                                        Faculty Review Portal
                                    </p>


                                </td>

                            </tr>

                        </table>

                        <!-- ================================= -->
                        <!-- END INNER CARD -->
                        <!-- ================================= -->


                    </td>

                </tr>

            </table>

            <!-- ============================================= -->
            <!-- END MAIN CARD -->
            <!-- ============================================= -->


        </td>

    </tr>

</table>

<!-- ===================================================== -->
<!-- END OUTER CONTAINER -->
<!-- ===================================================== -->


</body>

</html>
"""


# =========================================================
# STUDENT THANK YOU EMAIL
# =========================================================

def send_student_thank_you(review):
    """
    Send thank-you email to the student.

    IMPORTANT:
    No image attachment is added.

    The email only contains the designed HTML
    with the website background image.
    """

    student_name = review.student_name
    student_email = review.student_email

    # -----------------------------------------------------
    # CHECK EMAIL
    # -----------------------------------------------------

    if not student_email:

        print(
            "⚠️ No student email. "
            "Thank-you email skipped."
        )

        return

    print(
        "🔥 STUDENT THANK-YOU EMAIL FUNCTION RUNNING 🔥"
    )

    # -----------------------------------------------------
    # SUBJECT
    # -----------------------------------------------------

    subject = "Thank You for Your Feedback"

    # -----------------------------------------------------
    # PLAIN TEXT VERSION
    # -----------------------------------------------------

    text_message = f"""
Hello {student_name},

Thank you for submitting your feedback.

Your review has been successfully received.

Regards,
Faculty Review Portal
"""

    # -----------------------------------------------------
    # CREATE EMAIL
    # -----------------------------------------------------

    email = EmailMultiAlternatives(
        subject=subject,

        body=text_message,

        from_email=settings.DEFAULT_FROM_EMAIL,

        to=[student_email],
    )

    # -----------------------------------------------------
    # BACKGROUND IMAGE URL
    # -----------------------------------------------------

    background_url = (
        settings.SITE_URL.rstrip("/")
        + "/static/images/email_background.png"
    )

    print(
        "🖼️ Student email background URL:"
    )

    print(
        background_url
    )

    # -----------------------------------------------------
    # BUILD HTML
    # -----------------------------------------------------

    html_message = build_background_email_html(

        background_url=background_url,

        title="Thank You!",

        message=(
            f"{student_name}, "
            "your review has been received successfully."
        ),

        description=(
            "Thank you for taking the time "
            "to share your feedback with me."
        ),

        button_text="Feedback Received",

        button_url=None,
    )

    # -----------------------------------------------------
    # ATTACH HTML
    # -----------------------------------------------------

    email.attach_alternative(
        html_message,
        "text/html",
    )

    # -----------------------------------------------------
    # SEND
    # -----------------------------------------------------

    send_via_gmail_api(email)

    print(
        f"✅ Student thank-you email sent to "
        f"{student_email}"
    )


# =========================================================
# ADMIN NOTIFICATION EMAIL
# =========================================================

def send_admin_notification(
    review,
    admin_login_url=None,
):
    """
    Send admin notification email.

    Uses the SAME background design as the
    student thank-you email.

    IMPORTANT:
    No image attachment is added.
    """

    student_name = review.student_name

    print(
        "🔥 ADMIN EMAIL FUNCTION RUNNING 🔥"
    )

    # -----------------------------------------------------
    # SUBJECT
    # -----------------------------------------------------

    subject = "New Review Submitted"

    # -----------------------------------------------------
    # PLAIN TEXT VERSION
    # -----------------------------------------------------

    text_message = f"""
New Review Submitted

Hello Admin,

{student_name} has submitted a new review
through the Faculty Review Portal.

A new feedback response is waiting for you.

Login to the portal to review the feedback.

Regards,
Faculty Review Portal
"""

    # -----------------------------------------------------
    # CREATE EMAIL
    # -----------------------------------------------------

    email = EmailMultiAlternatives(

        subject=subject,

        body=text_message,

        from_email=settings.DEFAULT_FROM_EMAIL,

        to=[settings.ADMIN_EMAIL],
    )

    # -----------------------------------------------------
    # ADMIN LOGIN URL
    # -----------------------------------------------------

    if not admin_login_url:

        admin_login_url = (
            getattr(
                settings,
                "SITE_URL",
                "http://127.0.0.1:8000",
            ).rstrip("/")
            + "/admin-login/"
        )

    # -----------------------------------------------------
    # BACKGROUND IMAGE URL
    # -----------------------------------------------------

    background_url = (
        settings.SITE_URL.rstrip("/")
        + "/static/images/email_background.png"
    )

    print(
        "🖼️ Admin email background URL:"
    )

    print(
        background_url
    )

    # -----------------------------------------------------
    # BUILD SAME HTML DESIGN
    # -----------------------------------------------------

    html_message = build_background_email_html(

        background_url=background_url,

        title="New Review Submitted",

        message=(
            f"{student_name} has submitted "
            "a new review."
        ),

        description=(
            "A new feedback response is waiting "
            "for you in the Faculty Review Portal. "
            "Login to review the complete feedback."
        ),

        button_text="Admin Login",

        button_url=admin_login_url,
    )

    # -----------------------------------------------------
    # ATTACH HTML
    # -----------------------------------------------------

    email.attach_alternative(
        html_message,
        "text/html",
    )

    # -----------------------------------------------------
    # SEND
    # -----------------------------------------------------

    send_via_gmail_api(email)

    print(
        "✅ ADMIN EMAIL SENT SUCCESSFULLY"
    )
