from pathlib import Path
import base64
import html
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

    access_token = token_data.get("access_token")

    if not access_token:
        raise RuntimeError(
            "Gmail access token was not returned."
        )

    # -----------------------------------------------------
    # CONVERT DJANGO EMAIL INTO MIME
    # -----------------------------------------------------

    mime_message = email_message.message()

    raw_message = base64.urlsafe_b64encode(
        mime_message.as_bytes()
    ).decode("utf-8").rstrip("=")

    # -----------------------------------------------------
    # SEND THROUGH GMAIL API
    # -----------------------------------------------------

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
    Both emails use exactly the same:

    - Main card width
    - Inner card width
    - Card height
    - Padding
    - Typography
    - Button structure
    - Background structure

    Only the actual text/content changes.
    """

    # -----------------------------------------------------
    # SAFELY ESCAPE CONTENT
    # -----------------------------------------------------

    safe_title = html.escape(str(title))
    safe_message = html.escape(str(message))
    safe_description = html.escape(str(description))
    safe_button_text = html.escape(str(button_text))

    if button_url:
        safe_button_url = html.escape(
            str(button_url),
            quote=True
        )
    else:
        safe_button_url = "#"

    # -----------------------------------------------------
    # COMMON BUTTON
    # -----------------------------------------------------
    #
    # IMPORTANT:
    # Student and Admin both use the SAME <a> structure.
    #
    # Admin:
    #     href = actual admin URL
    #
    # Student:
    #     href = #
    #
    # Visual structure remains identical.
    # -----------------------------------------------------

    button_html = f"""
        <table
            width="auto"
            cellpadding="0"
            cellspacing="0"
            border="0"
            align="center"
            style="
                margin:0 auto 28px auto;
                border-collapse:collapse;
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
                        href="{safe_button_url}"
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
                        {safe_button_text}
                    </a>

                </td>

            </tr>

        </table>
    """

    # =====================================================
    # COMPLETE EMAIL HTML
    # =====================================================

    return f"""
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>{safe_title}</title>


    <style>

        /* =================================================
           GLOBAL RESET
           ================================================= */

        html,
        body {{
            margin:0 !important;
            padding:0 !important;

            width:100% !important;

            font-family:
                Arial,
                Helvetica,
                sans-serif;

            -webkit-text-size-adjust:100%;
            -ms-text-size-adjust:100%;
        }}


        body {{
            background:#eef3f8;
        }}


        table {{
            border-collapse:collapse;
            border-spacing:0;
        }}


        td {{
            border-collapse:collapse;
        }}


        img {{
            border:0;
            outline:none;
            text-decoration:none;
            display:block;
        }}


        /* =================================================
           MAIN CARD
           ================================================= */

        .email-main-card {{
            width:600px !important;

            min-width:600px !important;

            max-width:600px !important;

            margin:0 auto !important;

            table-layout:fixed;
        }}


        /* =================================================
           BACKGROUND AREA
           ================================================= */

        .email-background-cell {{
            width:600px !important;

            min-width:600px !important;

            max-width:600px !important;

            box-sizing:border-box;
        }}


        /* =================================================
           INNER WHITE CARD
           ================================================= */

        .email-inner-card {{
            width:530px !important;

            min-width:530px !important;

            max-width:530px !important;

            height:420px !important;

            min-height:420px !important;

            max-height:420px !important;

            table-layout:fixed;
        }}


        .email-inner-cell {{
            width:530px !important;

            min-width:530px !important;

            max-width:530px !important;

            height:420px !important;

            min-height:420px !important;

            max-height:420px !important;

            box-sizing:border-box;
        }}

    </style>

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


<!-- =====================================================
     OUTER EMAIL CONTAINER
     ===================================================== -->

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"

    style="
        width:100%;

        margin:0;
        padding:35px 10px;

        background:#eef3f8;

        border-collapse:collapse;
    "
>

    <tr>

        <td
            align="center"
            valign="top"
        >


            <!-- =============================================
                 MAIN WHITE CARD
                 ============================================= -->

            <table
                width="600"
                cellpadding="0"
                cellspacing="0"
                border="0"
                align="center"

                class="email-main-card"

                style="
                    width:600px;

                    min-width:600px;

                    max-width:600px;

                    margin:0 auto;

                    background:#ffffff;

                    border-radius:22px;

                    overflow:hidden;

                    border-collapse:collapse;

                    table-layout:fixed;
                "
            >

                <tr>

                    <td
                        valign="middle"
                        align="center"

                        class="email-background-cell"

                        style="
                            width:600px;

                            min-width:600px;

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

                            box-sizing:border-box;
                        "
                    >


                        <!-- =================================
                             INNER WHITE CARD
                             ================================= -->

                        <table
                            width="530"
                            cellpadding="0"
                            cellspacing="0"
                            border="0"
                            align="center"

                            class="email-inner-card"

                            style="
                                width:530px;

                                min-width:530px;

                                max-width:530px;

                                height:420px;

                                min-height:420px;

                                max-height:420px;

                                margin:0 auto;

                                background:#ffffff;

                                border-radius:18px;

                                border-collapse:collapse;

                                table-layout:fixed;
                            "
                        >

                            <tr>

                                <td
                                    align="center"
                                    valign="middle"

                                    class="email-inner-cell"

                                    style="
                                        width:530px;

                                        min-width:530px;

                                        max-width:530px;

                                        height:420px;

                                        min-height:420px;

                                        max-height:420px;

                                        box-sizing:border-box;

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


                                    <!-- =================================
                                         TITLE
                                         ================================= -->

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
                                        {safe_title}
                                    </h1>


                                    <!-- =================================
                                         BLUE LINE
                                         ================================= -->

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

                                            border-collapse:
                                                collapse;
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


                                    <!-- =================================
                                         MAIN MESSAGE
                                         ================================= -->

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
                                        {safe_message}
                                    </p>


                                    <!-- =================================
                                         DESCRIPTION
                                         ================================= -->

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
                                        {safe_description}
                                    </p>


                                    <!-- =================================
                                         BUTTON
                                         ================================= -->

                                    {button_html}


                                    <!-- =================================
                                         FOOTER
                                         ================================= -->

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

                        <!-- =================================
                             END INNER WHITE CARD
                             ================================= -->


                    </td>

                </tr>

            </table>

            <!-- =============================================
                 END MAIN CARD
                 ================================= -->


        </td>

    </tr>

</table>


<!-- =====================================================
     END OUTER EMAIL CONTAINER
     ===================================================== -->


</body>

</html>
"""


# =========================================================
# STUDENT THANK YOU EMAIL
# =========================================================

def send_student_thank_you(review):
    """
    Send thank-you email to the student.

    Uses the exact same HTML structure
    as the admin notification email.
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
            f"Thank you, {student_name}."
        ),

        description=(
            "Your feedback has been received successfully. "
            "Thank you for taking the time to share "
            "your feedback with me."
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

    Uses the exact same HTML structure
    as the student thank-you email.
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
    # BUILD HTML
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
