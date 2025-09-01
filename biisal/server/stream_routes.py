# Taken from megadlbot_oss <https://github.com/eyaadh/megadlbot_oss/blob/master/mega/webserver/routes.py>
# Thanks to Eyaadh <https://github.com/eyaadh>
# Thanks to adarsh-goel
# (c) @biisal
import re
import time
import math
import logging
import secrets
import mimetypes
from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine
from biisal.bot import multi_clients, work_loads, StreamBot
from biisal.server.exceptions import FIleNotFound, InvalidHash
from biisal import StartTime, __version__
from ..utils.time_format import get_readable_time
from ..utils.custom_dl import ByteStreamer
from biisal.utils.render_template import render_page
from biisal.vars import Var


routes = web.RouteTableDef()

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to AV Disk</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #1a0635, #0d0514);
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Animated background elements */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }
        
        .bg-circle {
            position: absolute;
            border-radius: 50%;
            background: rgba(92, 17, 165, 0.1);
            animation: float 15s infinite linear;
        }
        
        .bg-circle:nth-child(1) {
            width: 300px;
            height: 300px;
            top: -150px;
            left: -150px;
            animation-delay: 0s;
            animation-duration: 25s;
        }
        
        .bg-circle:nth-child(2) {
            width: 200px;
            height: 200px;
            bottom: -100px;
            right: 20%;
            animation-delay: 2s;
            animation-duration: 20s;
        }
        
        .bg-circle:nth-child(3) {
            width: 150px;
            height: 150px;
            top: 30%;
            right: -75px;
            animation-delay: 4s;
            animation-duration: 15s;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 50px;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            background: rgba(20, 5, 36, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .header.scrolled {
            padding: 15px 50px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
        }
        
        .logo {
            font-size: 1.8em;
            font-weight: 700;
            display: flex;
            align-items: center;
        }
        
        .logo i {
            margin-right: 10px;
            color: #9C27B0;
            background: white;
            padding: 5px;
            border-radius: 50%;
            transition: transform 0.3s ease;
        }
        
        .logo:hover i {
            transform: rotate(360deg);
        }
        
        .nav-links {
            display: flex;
            gap: 30px;
            align-items: center;
        }
        
        .nav-links a {
            color: #fff;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
            position: relative;
        }
        
        .nav-links a:after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: #BA68C8;
            transition: width 0.3s ease;
        }
        
        .nav-links a:hover {
            color: #E1BEE7;
        }
        
        .nav-links a:hover:after {
            width: 100%;
        }
        
        .signup-button {
            padding: 10px 20px;
            font-size: 1em;
            background: #7c1fd4;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .signup-button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(124, 31, 212, 0.4);
            background: #8e35e6;
        }
        
        .main-content {
            padding: 150px 50px 100px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        
        .hero {
            max-width: 800px;
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 4em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
            animation: fadeIn 1s ease;
            color: #fff;
        }
        
        .hero p {
            font-size: 1.5em;
            margin-bottom: 15px;
            text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.3);
            color: #E1BEE7;
        }
        
        .hero-subtext {
            font-size: 1.1em;
            color: #D1C4E9;
            max-width: 600px;
            margin: 0 auto 30px;
            line-height: 1.6;
        }
        
        .hero-buttons {
            display: flex;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .features {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 60px;
            flex-wrap: wrap;
        }
        
        .feature-card {
            background: rgba(63, 13, 112, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 25px;
            width: 250px;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .feature-card:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, rgba(156, 39, 176, 0.4), transparent);
            transform: translateY(100%);
            transition: transform 0.3s ease;
            z-index: -1;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        
        .feature-card:hover:before {
            transform: translateY(0);
        }
        
        .feature-card i {
            font-size: 2.5em;
            margin-bottom: 15px;
            color: #BA68C8;
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover i {
            transform: scale(1.2);
        }
        
        .feature-card h3 {
            margin-bottom: 10px;
            font-size: 1.4em;
            color: #fff;
        }
        
        .feature-card p {
            color: #D1C4E9;
            transition: color 0.3s ease;
        }
        
        .feature-card:hover p {
            color: #fff;
        }
        
        .buttons-container {
            display: flex;
            gap: 20px;
            margin-top: 30px;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .cta-button {
            padding: 18px 30px;
            font-size: 1.2em;
            background: #7c1fd4;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            gap: 10px;
            position: relative;
            overflow: hidden;
        }
        
        .cta-button:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, rgba(255, 255, 255, 0.2), transparent);
            transform: translateX(-100%);
            transition: transform 0.3s ease;
        }
        
        .cta-button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            background: #8e35e6;
        }
        
        .cta-button:hover:before {
            transform: translateX(100%);
        }
        
        .upload-button {
            background: linear-gradient(45deg, #FF5722, #E91E63);
        }
        
        .upload-button:hover {
            background: linear-gradient(45deg, #E64A19, #C2185B);
        }
        
        .floating-disks {
            position: relative;
            width: 100%;
            height: 200px;
            margin: 50px 0;
        }
        
        .disk {
            position: absolute;
            width: 100px;
            height: 100px;
            background: rgba(92, 17, 165, 0.3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 3px solid #BA68C8;
            animation: float 6s infinite ease-in-out;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .disk:hover {
            transform: scale(1.1);
            box-shadow: 0 0 30px rgba(186, 104, 200, 0.5);
            z-index: 100;
        }
        
        .disk:nth-child(1) {
            top: 0;
            left: 15%;
            animation-delay: 0s;
        }
        
        .disk:nth-child(2) {
            top: 20px;
            right: 15%;
            animation-delay: 1s;
        }
        
        .disk:nth-child(3) {
            bottom: 0;
            left: 25%;
            animation-delay: 2s;
        }
        
        .disk:nth-child(4) {
            bottom: 30px;
            right: 25%;
            animation-delay: 3s;
        }
        
        .disk i {
            font-size: 2em;
            color: #E1BEE7;
        }
        
        /* Testimonials Section */
        .testimonials {
            width: 100%;
            max-width: 1200px;
            margin: 60px 0;
        }
        
        .testimonials h2 {
            font-size: 2.5em;
            margin-bottom: 40px;
            color: #fff;
            text-align: center;
        }
        
        .testimonial-cards {
            display: flex;
            gap: 30px;
            overflow-x: auto;
            padding: 20px 0;
            scrollbar-width: thin;
            scrollbar-color: #7c1fd4 transparent;
        }
        
        .testimonial-cards::-webkit-scrollbar {
            height: 8px;
        }
        
        .testimonial-cards::-webkit-scrollbar-thumb {
            background: #7c1fd4;
            border-radius: 4px;
        }
        
        .testimonial-card {
            background: rgba(63, 13, 112, 0.4);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 25px;
            min-width: 300px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .testimonial-text {
            font-style: italic;
            margin-bottom: 20px;
            color: #D1C4E9;
            line-height: 1.6;
        }
        
        .testimonial-author {
            display: flex;
            align-items: center;
        }
        
        .author-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #BA68C8;
            margin-right: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
        
        .author-details {
            display: flex;
            flex-direction: column;
        }
        
        .author-name {
            font-weight: 600;
            color: #fff;
        }
        
        .author-title {
            font-size: 0.9em;
            color: #D1C4E9;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 50px;
            margin: 60px 0;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 3em;
            font-weight: 700;
            color: #fff;
            margin-bottom: 10px;
        }
        
        .stat-label {
            color: #D1C4E9;
            font-size: 1.1em;
        }
        
        .footer {
            margin-top: 50px;
            padding: 40px 20px;
            text-align: center;
            font-size: 0.9em;
            background: rgba(0, 0, 0, 0.3);
            width: 100%;
            color: #D1C4E9;
        }
        
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .footer-links {
            display: flex;
            gap: 30px;
            margin: 20px 0;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .footer-links a {
            color: #fff;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .footer-links a:hover {
            color: #E1BEE7;
            text-decoration: underline;
        }
        
        .social-links {
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }
        
        .social-links a {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            transition: all 0.3s ease;
        }
        
        .social-links a:hover {
            background: #7c1fd4;
            color: #fff;
            transform: translateY(-5px);
        }
        
        .copyright {
            margin-top: 20px;
            color: #D1C4E9;
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0) rotate(0deg);
            }
            50% {
                transform: translateY(-20px) rotate(10deg);
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Mobile menu */
        .menu-toggle {
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 30px;
            height: 30px;
            cursor: pointer;
        }
        
        .menu-toggle span {
            width: 100%;
            height: 3px;
            background: #fff;
            margin: 3px 0;
            transition: all 0.3s ease;
            border-radius: 3px;
        }
        
        @media (max-width: 968px) {
            .nav-links {
                position: fixed;
                top: 70px;
                left: 0;
                width: 100%;
                background: rgba(20, 5, 36, 0.95);
                flex-direction: column;
                align-items: center;
                padding: 20px;
                gap: 20px;
                transform: translateY(-100%);
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }
            
            .nav-links.active {
                transform: translateY(0);
                opacity: 1;
                visibility: visible;
            }
            
            .menu-toggle {
                display: flex;
            }
            
            .menu-toggle.active span:nth-child(1) {
                transform: rotate(45deg) translate(5px, 5px);
            }
            
            .menu-toggle.active span:nth-child(2) {
                opacity: 0;
            }
            
            .menu-toggle.active span:nth-child(3) {
                transform: rotate(-45deg) translate(7px, -6px);
            }
        }
        
        @media (max-width: 768px) {
            .header {
                padding: 15px 20px;
            }
            
            .header.scrolled {
                padding: 10px 20px;
            }
            
            .main-content {
                padding: 130px 20px 50px;
            }
            
            h1 {
                font-size: 2.5em;
            }
            
            .hero p {
                font-size: 1.2em;
            }
            
            .feature-card {
                width: 100%;
                max-width: 300px;
            }
            
            .hero-buttons, .buttons-container {
                flex-direction: column;
                align-items: center;
            }
            
            .cta-button {
                width: 100%;
                max-width: 300px;
                justify-content: center;
            }
            
            .stats {
                gap: 30px;
            }
            
            .stat-number {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <!-- Animated background elements -->
    <div class="bg-animation">
        <div class="bg-circle"></div>
        <div class="bg-circle"></div>
        <div class="bg-circle"></div>
    </div>

    <header class="header">
        <div class="logo">
            <i class="fas fa-photo-video"></i>
            <span>AV Disk</span>
        </div>
        
        <nav class="nav-links">
            <a href="#features">Features</a>
            <a href="#testimonials">Testimonials</a>
            <a href="#stats">Stats</a>
            <button class="signup-button" onclick="window.open('https://t.me/iPapcornPrimeGroup', '_blank')">
                Sign Up <i class="fas fa-user-plus"></i>
            </button>
        </nav>
        
        <div class="menu-toggle">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </header>

    <main class="main-content">
        <section class="hero">
            <h1>Welcome To AV Disk!</h1>
            <p>Your ultimate destination for streaming and sharing videos!</p>
            <p>Explore a world of entertainment at your fingertips.</p>
            
            <div class="hero-subtext">
                AV Disk offers the best platform for uploading, storing, and sharing your video content with the world. 
                Join thousands of satisfied users today!
            </div>
            
            <div class="hero-buttons">
                <button class="cta-button upload-button" onclick="window.open('https://t.me/iPapcornPrimeGroup', '_blank')">
                    Upload Your Media <i class="fas fa-upload"></i>
                </button>
            </div>
        </section>

        <div class="floating-disks">
            <div class="disk"><i class="fas fa-play"></i></div>
            <div class="disk"><i class="fas fa-film"></i></div>
            <div class="disk"><i class="fas fa-music"></i></div>
            <div class="disk"><i class="fas fa-share-alt"></i></div>
        </div>

        <section class="features" id="features">
            <div class="feature-card">
                <i class="fas fa-cloud-upload-alt"></i>
                <h3>Easy Upload</h3>
                <p>Upload your videos in seconds with our intuitive interface. Support for all major formats.</p>
            </div>
            <div class="feature-card">
                <i class="fas fa-bolt"></i>
                <h3>Fast Streaming</h3>
                <p>Enjoy buffer-free streaming with our optimized technology. Adaptive bitrate for all connections.</p>
            </div>
            <div class="feature-card">
                <i class="fas fa-lock"></i>
                <h3>Secure Storage</h3>
                <p>Your content is safe with our enterprise-grade security. Regular backups and encryption.</p>
            </div>
        </section>

        <div class="buttons-container">
            <button class="cta-button" onclick="window.open('https://t.me/iPapcornPrimeGroup', '_blank')">
                Get Started <i class="fas fa-arrow-right"></i>
            </button>
        </div>

        <section class="testimonials" id="testimonials">
            <h2>What Our Users Say</h2>
            <div class="testimonial-cards">
                <div class="testimonial-card">
                    <div class="testimonial-text">
                        "AV Disk has completely transformed how I share videos with my team. The streaming quality is exceptional!"
                    </div>
                    <div class="testimonial-author">
                        <div class="author-avatar">JD</div>
                        <div class="author-details">
                            <div class="author-name">John Doe</div>
                            <div class="author-title">Content Creator</div>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-text">
                        "I've tried many platforms, but AV Disk's upload speed and reliability are unmatched. Highly recommend!"
                    </div>
                    <div class="testimonial-author">
                        <div class="author-avatar">SM</div>
                        <div class="author-details">
                            <div class="author-name">Sarah Miller</div>
                            <div class="author-title">Video Editor</div>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-text">
                        "The security features give me peace of mind when storing my sensitive video content. Great platform!"
                    </div>
                    <div class="testimonial-author">
                        <div class="author-avatar">RJ</div>
                        <div class="author-details">
                            <div class="author-name">Robert Johnson</div>
                            <div class="author-title">Photographer</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="stats" id="stats">
            <div class="stat-item">
                <div class="stat-number">5K+</div>
                <div class="stat-label">Active Users</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">50K+</div>
                <div class="stat-label">Videos Uploaded</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">99.9%</div>
                <div class="stat-label">Uptime</div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="footer-content">
            <div class="logo">
                <i class="fas fa-photo-video"></i>
                <span>AV Disk</span>
            </div>
            <div class="footer-links">
                <a href="#">Home</a>
                <a href="#features">Features</a>
                <a href="#testimonials">Testimonials</a>
                <a href="#stats">Stats</a>
                <a href="#">Privacy Policy</a>
                <a href="#">Terms of Service</a>
            </div>
            <div class="social-links">
                <a href="#"><i class="fab fa-facebook-f"></i></a>
                <a href="#"><i class="fab fa-twitter"></i></a>
                <a href="#"><i class="fab fa-instagram"></i></a>
                <a href="#"><i class="fab fa-linkedin-in"></i></a>
            </div>
            <div class="copyright">
                &copy; AV Disk. All rights reserved 2025.
            </div>
        </div>
    </footer>

    <script>
        // Header scroll effect
        window.addEventListener('scroll', function() {
            const header = document.querySelector('.header');
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
        
        // Mobile menu toggle
        const menuToggle = document.querySelector('.menu-toggle');
        const navLinks = document.querySelector('.nav-links');
        
        menuToggle.addEventListener('click', function() {
            menuToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on links
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });
    </script>
</body>
</html>"""

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text=html_content, content_type='text/html')



@routes.get(r"/watch/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return web.Response(text=await render_page(id, secure_hash), content_type='text/html')
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))

@routes.get(r"/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return await media_streamer(request, id, secure_hash)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))

class_cache = {}

async def media_streamer(request: web.Request, id: int, secure_hash: str):
    range_header = request.headers.get("Range", 0)
    
    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]
    
    if Var.MULTI_CLIENT:
        logging.info(f"Client {index} is now serving {request.remote}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
        logging.debug(f"Using cached ByteStreamer object for client {index}")
    else:
        logging.debug(f"Creating new ByteStreamer object for client {index}")
        tg_connect = ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect
    logging.debug("before calling get_file_properties")
    file_id = await tg_connect.get_file_properties(id)
    logging.debug("after calling get_file_properties")
    
    if file_id.unique_id[:6] != secure_hash:
        logging.debug(f"Invalid hash for message with ID {id}")
        raise InvalidHash
    
    file_size = file_id.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = (request.http_range.stop or file_size) - 1

    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    chunk_size = 1024 * 1024
    until_bytes = min(until_bytes, file_size - 1)

    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil(until_bytes / chunk_size) - math.floor(offset / chunk_size)
    body = tg_connect.yield_file(
        file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
    )

    mime_type = file_id.mime_type
    file_name = file_id.file_name
    disposition = "attachment"

    if mime_type:
        if not file_name:
            try:
                file_name = f"{secrets.token_hex(2)}.{mime_type.split('/')[1]}"
            except (IndexError, AttributeError):
                file_name = f"{secrets.token_hex(2)}.unknown"
    else:
        if file_name:
            mime_type = mimetypes.guess_type(file_id.file_name)
        else:
            mime_type = "application/octet-stream"
            file_name = f"{secrets.token_hex(2)}.unknown"

    return web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": f"{mime_type}",
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(req_length),
            "Content-Disposition": f'{disposition}; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        },
    )

