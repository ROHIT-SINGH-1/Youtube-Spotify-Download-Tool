import os
import subprocess
import datetime
from pytube import YouTube
import validators
import requests
import time
import sys

# DOWNLOAD_DIRECTORY =   # Change this to your desired directory
DOWNLOAD_DIRECTORY = os.path.join(os.path.expanduser("~"), "Downloads")

# Get the absolute path of the download directory and video folder
download_directory = os.path.abspath(DOWNLOAD_DIRECTORY)

# Create the download directory and video folder if they don't exist
os.makedirs(download_directory, exist_ok=True)

# Display the absolute paths (optional, for confirmation)

session = requests.Session()

start_time = time.time()


def progress_bar(
    iteration, total, start_time=None, prefix="", suffix="", decimals=1, length=20
):
    if start_time is None:
        start_time = time.time()

    percent = 100 * (iteration / float(total))
    percent = min(percent, 100.0)  # Ensure percent doesn't exceed 100
    iteration = min(iteration, total)

    filled_length = int(length * iteration // total)
    elapsed_time = time.time() - start_time

    if elapsed_time < 60:
        time_format = f"{elapsed_time:.1f} sec"
    else:
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_format = f"{minutes:.0f} min {seconds:.1f} sec"

    if percent < 30:
        color = "\033[91m"  # Red
    elif percent < 50:
        color = "\033[93m"  # Yellow
    elif percent < 75:
        color = "\033[92m"  # Green
    else:
        color = "\033[94m"  # Blue

    end_color = "\033[0m"

    formatted_text = (
        f"\r\033[1m{prefix}[\033[1m\033[38;2;{color}{'=' * filled_length}\033[0m{'-' * (length - filled_length)}] "
        f"\033[1m\033[38;2;255;165;0m{percent:.{decimals}f}\033[0m\033[1m \033[38;2;255;165;0m- ETA {time_format}\033[0m {suffix}"
    )

    print(formatted_text, end="", flush=True)

    if iteration == total:
        print()


def clear_cookies(session):
    # Clear cookies by resetting the session
    session.cookies.clear()


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def clear_console():
    # Clear console screen
    if os.name == "nt":
        _ = os.system("cls")  # For Windows
    else:
        _ = os.system("clear")  # For Linux/MacOS


def download_from_spotify(url):
    global DOWNLOAD_DIRECTORY
    start_time = time.time()

    if not validators.url(url):
        print("\033[1m" + "\033[38;2;255;165;0m" + "INVALID SPOTIFY URL." + "\033[0m")
        return

    spotify_directory = os.path.join(DOWNLOAD_DIRECTORY, "SPOTIFY")
    create_directory(spotify_directory)

    try:
        clear_console()  # Clear console screen
        clear_cookies(session)
        print(
            "\033[1m" + "\033[38;2;255;165;0m" + "DOWNLOAD FROM SPOTIFY..." + "\033[0m"
        )

        # Prompt the user for audio codec choice
        print("\033[1m" + "\033[38;2;255;165;0m" + "CHOOSE AUDIO CODEC :" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "1. MP3" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "2. FLAC" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "3. OGG" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "4. OPUS" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "5. M4A" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "6. WAV" + "\033[0m")
        audio_codec_choice = input(
            "\033[1m" + "\033[38;2;255;165;0m" + "Enter the number: " + "\033[0m"
        )
        clear_console()

        audio_codecs = {
            "1": "mp3",
            "2": "flac",
            "3": "ogg",
            "4": "opus",
            "5": "m4a",
            "6": "wav",
            # Add more codec options as needed
        }

        audio_codec = audio_codecs.get(audio_codec_choice)
        if audio_codec is None:
            print(
                "\033[1m"
                + "\033[38;2;255;165;0m"
                + "INVALID AUDIO CODEC CHOOSE"
                + "\033[0m"
            )
            return

        # Prompt the user for audio bitrate choice
        print("\033[1m" + "\033[38;2;255;165;0m" + "CHOOSE AUDIO BITRATE:" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "1. 128K" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "2. 192K" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "3. 224K" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "4. 256K" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "5. 320K" + "\033[0m")
        # Add more bitrate options as needed
        audio_bitrates = {
            "1": "128k",
            "2": "192k",
            "3": "224k",
            "4": "256k",
            "5": "320k"
            # Add more bitrate options as needed
        }
        audio_bitrate_choice = input(
            "\033[1m" + "\033[38;2;255;165;0m" + "Enter the number: " + "\033[0m"
        )
        clear_console()

        audio_bitrate = audio_bitrates.get(audio_bitrate_choice)
        if audio_bitrate is None:
            print(
                "\033[1m"
                + "\033[38;2;255;165;0m"
                + "INVALID AUDIO BITRATE CHOOSE."
                + "\033[0m"
            )
            return

        # Capture output and error streams
        command = [
            "spotdl",
            url,
            "--output",
            spotify_directory,
            "--bitrate",
            audio_bitrate,
            "--format",
            audio_codec,
        ]
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        print(
            "\033[1m" + "\033[38;2;255;165;0m" + "DOWNLOAD FROM SPOTIFY..." + "\033[0m"
        )

        # Read output and error lines
        while True:
            output = process.stdout.readline()
            error = process.stderr.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                # Check if the line contains progress info and print it
                if "SPOTIFY DOWNLOAD:" in output:
                    print(output.strip())  # Print the progress line
            if error:
                print(
                    f"\033[1m" + "\033[38;2;255;165;0m" + "ERROR: {error}" + "\033[0m"
                )  # Print any error messages

        # Show progress bar after reading output
        for i in range(101):
            time.sleep(
                0.1
            )  # Simulate progress - Adjust time for smoother or faster progress
            progress_bar(
                i,
                100,
                start_time,
                prefix="\033[1m"
                + "\033[38;2;255;165;0m"
                + "SPOTIFY DOWNLOAD: "
                + "\033[0m",
                suffix=" ",
                length=20,
            )

        print(
            "\033[1m"
            + "\033[38;2;255;165;0m"
            + "\nDOWNLOAD FROM SPOTIFY COMPLETED."
            + "\033[0m"
        )
    except subprocess.CalledProcessError as e:
        print(
            f"\033[1m"
            + "\033[38;2;255;165;0m"
            + "ERROR DOWNLOAD FROM SPOTIFY: {e.stderr}"
        )
    except Exception as e:
        print(f"\033[1m" + "\033[38;2;255;165;0m" + "UNEXPECTED ERROR: {e}" + "\033[0m")


def validate_youtube_url(url):
    if not validators.url(url):
        print("\033[1m" + "\033[38;2;255;165;0m" + "INVALID YOUTUBE URL." + "\033[0m")
        return False
    return True


def sanitize_filename(filename):
    # Replace special characters with an underscore
    filename = "".join(c if c.isalnum() or c in [" ", "."] else "_" for c in filename)
    # Replace multiple spaces with a single space
    filename = " ".join(filename.split())
    return filename


def download_from_youtube(url, download_directory):
    start_time = time.time()
    if not validate_youtube_url(url):
        return

    youtube_directory = os.path.join(download_directory, "YOUTUBE")
    create_directory(youtube_directory)

    try:
        clear_console()
        clear_cookies(session)

        # Prompt the user for video codec choice
        print("\033[1m" + "\033[38;2;255;165;0m" + "CHOOSE VIDEO CODEC" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "1. H.264" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "2. VP9" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "2. H.265" + "\033[0m")
        video_codec_choice = input(
            "\033[1m" + "\033[38;2;255;165;0m" + "ENTER THE NUMBER: " + "\033[0m"
        )
        clear_console()

        video_codecs = {
            "1": "h264",
            "2": "vp9",
            "3": "h265",
            # Add more codec options as needed
        }

        video_codec = video_codecs.get(video_codec_choice)
        if video_codec is None:
            print("\033[1m" + "\033[38;2;255;165;0m" + "INVALID CHOICE" + "\033[0m")
            return

        # Prompt the user for audio codec choice
        print("\033[1m" + "\033[38;2;255;165;0m" + "CHOOSE AUDIO CODEC:" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "1. AAC" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "2. MP3" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "3. FLAC" + "\033[0m")
        audio_codec_choice = input(
            "\033[38;2;255;165;0m" + "ENTER THE NUMBER: " + "\033[0m"
        )
        clear_console()

        audio_codecs = {
            "1": "aac",
            "2": "mp3",
            "3": "flac"
            # Add more codec options as needed
        }

        audio_codec = audio_codecs.get(audio_codec_choice)
        if audio_codec is None:
            print("\033[38;2;255;165;0m" + "INVALID CHOICE" + "\033[0m")
            return

        # Prompt the user for frames per second (fps) choice
        print("\033[1m" + "\033[38;2;255;165;0m" + "CHOOSE FPS:" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "1. 24 FPS" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "2. 30 FPS" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "3. 60 FPS" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "4. 90 FPS" + "\033[0m")
        fps_choice = input("\033[38;2;255;165;0m" + "ENTER THE NUMBER: " + "\033[0m")
        clear_console()

        fps_options = {
            "1": "24",
            "2": "30",
            "3": "60",
            "4": "90"
            # Add more fps options as needed
        }

        fps = fps_options.get(
            fps_choice, "30"
        )  # Default to 30 fps if choice is invalid

        yt = YouTube(url)
        video_streams = yt.streams.filter(type="video").order_by("resolution").desc()

        # Display available video streams with resolutions
        print(
            "\033[1m" + "\033[38;2;255;165;0m" + "AVAILABLE VIDEO STREAMS" + "\033[0m"
        )

        resolutions = {}  # Store resolutions in a dictionary for accurate selection
        count = 1
        for stream in video_streams:
            if stream.resolution not in resolutions:
                resolutions[stream.resolution] = stream
                print(
                    "\033[1m"
                    + "\033[38;2;255;165;0m"
                    + f"{count}. RESOLUTION {stream.resolution}"
                    + "\033[0m"  # Bold and orange formatting for numbers
                )

                count += 1

        video_resolution_choice = input(
            "\033[1m" + "\033[38;2;255;165;0m" + "ENTER THE NUMBER:" + "\033[0m"
        )

        clear_console()
        # Prompt the user for encoding speed choice
        print("\033[1m" + "\033[38;2;255;165;0m" + "CHOOSE ENCODING SPEED:" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "1. SLOW" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "2. FAST" + "\033[0m")
        print("\033[1m" + "\033[38;2;255;165;0m" + "3. ULTRAFAST" + "\033[0m")
        encoding_speed_choice = input(
            "\033[1m" + "\033[38;2;255;165;0m" + "ENTER THE NUMBER: " + "\033[0m"
        )
        clear_console()

        encoding_speeds = {
            "3": "slow",
            "2": "fast",
            "1": "ultrafast"
            # Add more speed options as needed
        }

        encoding_speed = encoding_speeds.get(encoding_speed_choice)
        if encoding_speed is None:
            print(
                "\033[1m"
                + "\033[38;2;255;165;0m"
                + "INVALID ENCODEING SPEED CHOICE"
                + "\033[0m"
            )
            return

        try:
            selected_stream = resolutions.get(
                list(resolutions.keys())[int(video_resolution_choice) - 1]
            )
            if selected_stream:
                print(
                    f"\033[1m"
                    + "\033[38;2;255;165;0m"
                    + f"SELECTED: [{selected_stream.resolution}], VIDEO CODEC: [{video_codec}], "
                    f"AUDIO CODEC: [{audio_codec}], FRAME PER SECOND: [{fps}] FPS"
                    + "\033[0m"
                )

                audio_stream = yt.streams.filter(only_audio=True).first()

                if not selected_stream or not audio_stream:
                    print(
                        "\033[1m"
                        + "\033[38;2;255;165;0m"
                        + "VIDEO OR AUDIO NOT AVALABLE"
                        + "\033[0m"
                    )
                    return

                print(
                    "\033[1m"
                    + "\033[38;2;255;165;0m"
                    + "YOUTUBE VIDEO DOWNLOAD..."
                    + "\033[0m"
                )
                sanitized_title = sanitize_filename(yt.title)
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

                video_filename = (
                    f"{sanitized_title}_video_{timestamp}.{selected_stream.subtype}"
                )
                audio_filename = (
                    f"{sanitized_title}_audio_{timestamp}.{audio_stream.subtype}"
                )

                video_path = os.path.join(youtube_directory, video_filename)
                audio_path = os.path.join(youtube_directory, audio_filename)

                selected_stream.download(
                    output_path=youtube_directory, filename=video_filename
                )
                audio_stream.download(
                    output_path=youtube_directory, filename=audio_filename
                )

                merged_filename = f"{sanitized_title}_merged_{timestamp}.mp4"
                merged_path = os.path.join(youtube_directory, merged_filename)

                command = [
                    "ffmpeg",
                    "-i",
                    video_path,
                    "-i",
                    audio_path,
                    "-c:v",
                    video_codec,
                    "-c:a",
                    audio_codec,
                    "-b:a",
                    "1400k",
                    "-ar",
                    "48000",
                    "-preset",
                    encoding_speed,
                    "-r",
                    fps,  # Add the fps option
                    "-hide_banner",
                    "-loglevel",
                    "panic",
                    merged_path,
                ]
                subprocess.run(command, check=True)

                merged_filesize = (
                    100  # Replace with the actual merged file size or duration
                )
                for i in range(merged_filesize + 1):
                    progress_bar(
                        i,
                        merged_filesize,
                        start_time,
                        prefix="\033[1m"
                        + "\033[38;2;255;165;0m"
                        + "YOUTUBE: "
                        + "\033[0m",
                        suffix=" ",
                        length=20,
                    )
                    time.sleep(0.1)  # Simulating progress

                os.remove(video_path)
                os.remove(audio_path)
                print(
                    f"\033[1m"
                    + "\033[38;2;255;165;0m"
                    + f"\nDOWNLOAD YOUTUBE VIDEO COMPLETED... [{merged_filename}]"
                    + "\033[0m"
                )

                # print(f"\033[1m" + "\033[38;2;255;165;0m" + "DOWNLOAD DIRECTORY: {download_directory}"+ "\033[0m")
            else:
                print(
                    "\033[1m" + "\033[38;2;255;165;0m" + "INVALID CHOICE." + "\033[0m"
                )
                return
        except (ValueError, IndexError):
            print("\033[1m" + "\033[38;2;255;165;0m" + "INVALID CHOICE." + "\033[0m")
            return

    except Exception as e:
        print(f"\033[1m\033[38;2;255;165;0mERROR: {e}\033[0m")


def print_menu():
    print(
        "\033[1m"
        + "\033[38;2;255;165;0m"
        + "╔════════════════════════════╗"
        + "\033[0m"
    )
    print(
        "\033[1m"
        + "\033[38;2;255;165;0m"
        + "║      CHOOSE AN OPTION      ║"
        + "\033[0m"
    )
    print(
        "\033[1m"
        + "\033[38;2;255;165;0m"
        + "╠════════════════════════════╣"
        + "\033[0m"
    )
    print(
        "\033[1m"
        + "\033[38;2;255;165;0m"
        + "║  1. DOWNLOAD FROM SPOTIFY  ║"
        + "\033[0m"
    )
    print(
        "\033[1m"
        + "\033[38;2;255;165;0m"
        + "║  2. DOWNLOAD FROM YOUTUBE  ║"
        + "\033[0m"
    )
    print(
        "\033[1m"
        + "\033[38;2;255;165;0m"
        + "║  3. QUIT                   ║"
        + "\033[0m"
    )
    print(
        "\033[1m"
        + "\033[38;2;255;165;0m"
        + "╚════════════════════════════╝"
        + "\033[0m"
    )


def main():
    while True:
        clear_console()
        print_menu()

        choice = input(
            "\033[1m" + "\033[38;2;255;165;0m" + "ENTER THE NUMBER: " + "\033[0m"
        )

        if choice == "1":
            urls = input(
                "\033[1m"
                + "\033[38;2;255;165;0m"
                + "PLEASE ENTER SPOTIFY URLs -[MULTIPLE URLs USE SAPERATE BY COMMA]: "
                + "\033[0m"
            )
            url_list = [url.strip() for url in urls.split(",")]

            for url in url_list:
                if validators.url(url) and "spotify" in url.lower():
                    download_from_spotify(url)
                else:
                    print(
                        f"\033[1m\033[38;2;255;165;0mINVALID SPOTIFY URL.. : \033[0m\033[1m\033[91m[{url}]\033[0m\033[1m\033[38;2;255;165;0m. SKIPPING...\033[0m"
                    )

        elif choice == "2":
            urls = input(
                "\033[1m"
                + "\033[38;2;255;165;0m"
                + "PLEASE ENTER YOUTUBE URLs -[MULTIPLE URLs USE SAPERATE BY COMMA]: "
                + "\033[0m"
            )
            url_list = [url.strip() for url in urls.split(",")]

            for url in url_list:
                if validators.url(url) and (
                    "youtube.com" in url.lower() or "youtu.be" in url.lower()
                ):
                    download_from_youtube(url, DOWNLOAD_DIRECTORY)
                else:
                    print(
                        f"\033[1m\033[38;2;255;165;0mINVALID YOUTUBE URL: \033[0m\033[1m\033[91m{url}\033[0m\033[1m\033[38;2;255;165;0m. SKIPPING...\033[0m"
                    )

        elif choice == "3":
            clear_console()
            print("\033[1;38;2;255;165;0m   ▄▄▀▀█▀▀▄▄     ")
            print("  ▐▄▌ ▀ ▀ ▐▄▌    ")
            print("    █ ▄▄▄ █  ▄▄  ")
            print("    ▄█▄▄▄█▄ ▐  ▌ ")
            print("  ▄█▀█████▐▌ ▀ ▐ ")
            print("  ▀ ▄██▀██▀█▀▄▄▀ ")
            print("\033[1;38;2;255;165;0m ════════════════")
            print("\033[0m")  # Reset color/style
            print(
                "\033[1m" + "\033[38;2;255;165;0m" + " TOOL EXITING..." + "\033[0m"
            )  # take 24 space to make center this line
            time.sleep(5)
            sys.exit()
            # Exiting the terminal

        # Add an input prompt to pause at the end of each download
        input(
            "\033[1m"
            + "\033[38;2;255;165;0m"
            + "PRESS ENTER TO CONTINUE..."
            + "\033[0m"
        )

        # Ask the user if they want to download more songs
        more_songs = input(
            "\033[1m"
            + "\033[38;2;255;165;0m"
            + "DO YOU WANT TO DOWNLOAD MORE SONGS (Y/N): "
            + "\033[0m"
        ).lower()
        if more_songs != "y":
            print(
                "\033[1m"
                + "\033[38;2;255;165;0m"
                + "EXITING THE PROGRAM. GOODBYE!"
                + "\033[0m"
            )
            clear_console()
            print("\033[1;38;2;255;165;0m   ▄▄▀▀█▀▀▄▄     ")
            print("  ▐▄▌ ▀ ▀ ▐▄▌    ")
            print("    █ ▄▄▄ █  ▄▄  ")
            print("    ▄█▄▄▄█▄ ▐  ▌ ")
            print("  ▄█▀█████▐▌ ▀ ▐ ")
            print("  ▀ ▄██▀██▀█▀▄▄▀ ")
            print("\033[1;38;2;255;165;0m ════════════════")
            print("\033[0m")  # Reset color/style# Reset color/style
            print("\033[1m" + "\033[38;2;255;165;0m" + " TOOL EXITING..." + "\033[0m")
            time.sleep(5)
            break


if __name__ == "__main__":
    main()
