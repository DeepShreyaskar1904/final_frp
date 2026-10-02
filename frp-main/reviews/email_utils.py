from pathlib import Path
import base64
import requests
from io import BytesIO
from email.utils import make_msgid
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.message import MIMEPart
from email.mime.image import MIMEImage

BASE_DIR = Path(__file__).resolve().parent.parent
EMAIL_BACKGROUND_PATH = (
    BASE_DIR
    / "static"
    / "images"
    / "email_background.png"
)


def get_email_font(size, bold=False):
    paths = (
        [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
        if bold
        else [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
    )

    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def create_email_background():
    """Create a soft/faded version of the local logo image."""

    print("🖼️ Creating email background...")

    if not EMAIL_BACKGROUND_PATH.exists():
        print("❌ EMAIL BACKGROUND NOT FOUND:")
        print(EMAIL_BACKGROUND_PATH)
        return None

    try:
        background = Image.open(EMAIL_BACKGROUND_PATH).convert("RGB")

        WIDTH = 1200
        HEIGHT = 900

        ratio = max(
            WIDTH / background.width,
            HEIGHT / background.height,
        )

        new_size = (
            int(background.width * ratio),
            int(background.height * ratio),
        )

        background = background.resize(
            new_size,
            Image.Resampling.LANCZOS,
        )

        left = (background.width - WIDTH) // 2
        top = (background.height - HEIGHT) // 2

        background = background.crop(
            (
                left,
                top,
                left + WIDTH,
                top + HEIGHT,
            )
        )

        white = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            (255, 255, 255),
        )

        background = Image.blend(
            background,
            white,
            0.62,
        )

        output = BytesIO()
        background.save(
            output,
            format="PNG",
            optimize=True,
        )
        output.seek(0)

        print("✅ Faded email background created successfully")
        return output

    except Exception as e:
        print("❌ Email background creation error:", e)
        return None


def attach_inline_image(email_message, image_data):
    """Attach the email background as a real inline MIME image."""

    if image_data is None:
        return None

    cid = make_msgid()

    image_part = MIMEImage(
        image_data.getvalue(),
        _subtype="png",
    )

    image_part.add_header(
        "Content-ID",
        cid,
    )
    image_part.add_header(
        "Content-Disposition",
        "inline",
    )

    email_message.attach(image_part)

    return cid[1:-1]


def send_via_gmail_api(email_message):
    """Send an already-built Django email through the Gmail API."""

    refresh_token = getattr(settings, "GMAIL_REFRESH_TOKEN", "").strip()

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


    mime_message = email_message.message()
    raw_message = base64.urlsafe_b64encode(
        mime_message.as_bytes()
    ).decode("utf-8").rstrip("=")


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

    print("✅ Email sent successfully through Gmail API")

def build_background_email_html(
    cid,
    title,
    message,
    description,
    button_text,
    button_url,
):
    """
    SAME email design for both:
    - Student thank-you email
    - Admin notification email

    Fixed card size so both emails look identical in Gmail.
    """


    if button_url:
        button_html = f"""
        <table
            cellpadding="0"
            cellspacing="0"
            border="0"
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
                            font-family:Arial, Helvetica, sans-serif;
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
                            font-family:Arial, Helvetica, sans-serif;
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


    return f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>{title}</title>

</head>


<body
    style="
        margin:0;
        padding:0;
        background:#eef3f8;
        font-family:Arial, Helvetica, sans-serif;
    "
>

<!-- ===================================================== -->
<!-- OUTER EMAIL BACKGROUND -->
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


<!-- ===================================================== -->
<!-- FIXED MAIN CARD -->
<!-- ===================================================== -->

<table
    width="600"
    cellpadding="0"
    cellspacing="0"
    border="0"
    align="center"
    style="
        width:600px;
        max-width:600px;
        min-width:600px;
        margin:0 auto;
        background:#ffffff;
        border-radius:22px;
        overflow:hidden;
    "
>

<tr>

<td
    background="cid:{cid}"
    bgcolor="#f4f7fb"
    valign="middle"
    align="center"
    style="
        width:600px;
        max-width:600px;

        background-image:url('cid:{cid}');
        background-repeat:no-repeat;
        background-position:center;
        background-size:cover;

        padding:55px 35px;
    "
>


<!-- ===================================================== -->
<!-- INNER CONTENT CARD -->
<!-- ===================================================== -->

<table
    width="530"
    cellpadding="0"
    cellspacing="0"
    border="0"
    align="center"
    style="
        width:530px;
        max-width:530px;
        margin:0 auto;

        background:#ffffff;

        border-radius:18px;
    "
>

<tr>

<td
    align="center"
    valign="middle"
    style="
        padding:42px 38px 38px 38px;

        font-family:Arial, Helvetica, sans-serif;

        color:#172554;

        text-align:center;
    "
>


<!-- ===================================================== -->
<!-- TITLE -->
<!-- ===================================================== -->

<h1
    style="
        margin:0;
        padding:0;

        font-family:Arial, Helvetica, sans-serif;

        font-size:30px;
        line-height:38px;

        font-weight:700;

        color:#172554;

        text-align:center;
    "
>
    {title}
</h1>


<!-- ===================================================== -->
<!-- BLUE LINE -->
<!-- ===================================================== -->

<table
    cellpadding="0"
    cellspacing="0"
    border="0"
    align="center"
    style="
        margin:16px auto 24px auto;
    "
>

<tr>

<td
    width="65"
    height="5"
    style="
        width:65px;
        height:5px;

        background:#2563eb;

        border-radius:5px;

        font-size:0;
        line-height:0;
    "
>
    &nbsp;
</td>

</tr>

</table>


<!-- ===================================================== -->
<!-- MAIN MESSAGE -->
<!-- ===================================================== -->

<p
    style="
        margin:0 0 22px 0;
        padding:0;

        font-family:Arial, Helvetica, sans-serif;

        font-size:19px;
        line-height:30px;

        font-weight:700;

        color:#1e293b;

        text-align:center;
    "
>
    {message}
</p>


<!-- ===================================================== -->
<!-- DESCRIPTION -->
<!-- ===================================================== -->

<p
    style="
        margin:0 0 30px 0;
        padding:0;

        font-family:Arial, Helvetica, sans-serif;

        font-size:16px;
        line-height:27px;

        color:#64748b;

        text-align:center;
    "
>
    {description}
</p>


<!-- ===================================================== -->
<!-- BUTTON -->
<!-- ===================================================== -->

{button_html}


<!-- ===================================================== -->
<!-- FOOTER -->
<!-- ===================================================== -->

<p
    style="
        margin:0;
        padding:0;

        font-family:Arial, Helvetica, sans-serif;

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

<!-- ===================================================== -->
<!-- END INNER CARD -->
<!-- ===================================================== -->


</td>

</tr>

</table>

<!-- ===================================================== -->
<!-- END FIXED MAIN CARD -->
<!-- ===================================================== -->


</td>

</tr>

</table>

<!-- ===================================================== -->
<!-- END OUTER CONTAINER -->
<!-- ===================================================== -->

</body>

</html>
"""

def send_student_thank_you(review):
    """Send the student a thank-you email using the same logo background."""

    student_name = review.student_name
    student_email = review.student_email

    if not student_email:
        print("⚠️ No student email. Thank-you email skipped.")
        return

    subject = "Thank You for Your Feedback"

    text_message = f"""
Hello {student_name},

Thank you for submitting your feedback.

Your review has been successfully received.

Regards,
Faculty Review Portal
"""

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[student_email],
    )

    background_data = create_email_background()
    cid = attach_inline_image(email, background_data)

    if cid is None:
        print("❌ Student email background could not be created.")
        return

    html_message = build_background_email_html(
        cid=cid,
        title="Thank You!",
        message=f"{student_name}, your review has been received successfully.",
        description=(
            "Thank you for taking the time to share your feedback "
            "with me."
        ),
        button_text="Feedback Received",
        button_url=None,
    )

    email.attach_alternative(
        html_message,
        "text/html",
    )

    send_via_gmail_api(email)

    print(f"✅ Student thank-you email sent to {student_email}")


def send_admin_notification(
    review,
    admin_login_url=None,
):
    """
    Send admin notification using the SAME
    background-image email design as the student email.
    """

    student_name = review.student_name

    print("🔥 NEW ADMIN BACKGROUND EMAIL FUNCTION RUNNING 🔥")


    subject = "New Review Submitted"


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


    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMIN_EMAIL],
    )


    print("🖼️ Creating ADMIN email background...")

    background_data = create_email_background()

    if background_data is None:
        print("❌ Admin background image creation failed.")
        return

    print("✅ ADMIN background image created")


    cid = attach_inline_image(
        email,
        background_data
    )

    if cid is None:
        print("❌ Admin background image attachment failed.")
        return

    print("✅ ADMIN background image attached")


    if not admin_login_url:

        admin_login_url = (
            getattr(
                settings,
                "SITE_URL",
                "http://127.0.0.1:8000"
            ).rstrip("/")
            + "/admin-login/"
        )


    html_message = build_background_email_html(

        cid=cid,

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


    email.attach_alternative(
        html_message,
        "text/html"
    )


    send_via_gmail_api(email)

    print(
        "✅ ADMIN BACKGROUND EMAIL SENT SUCCESSFULLY"
    )
