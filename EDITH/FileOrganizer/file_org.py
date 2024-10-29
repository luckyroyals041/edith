import os
import shutil
from pathlib import Path

def organize_files(directory):
    """
    Organize files in the given directory by their extensions.
    """
    try:
        # Convert to absolute path and ensure it exists
        directory = os.path.abspath(directory)
        
        if not os.path.exists(directory):
            raise Exception(f"Directory does not exist: {directory}")
            
        if not os.path.isdir(directory):
            raise Exception(f"Path is not a directory: {directory}")
            
        # Create a Path object for the directory
        dir_path = Path(directory)
        
        # Get list of files before moving (excluding subdirectories)
        files_to_organize = [f for f in dir_path.iterdir() if f.is_file()]
        
        if not files_to_organize:
            return "No files found to organize"

        # Dictionary to map file extensions to folder names
        extension_map = {
            # Images
            '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images',
            '.bmp': 'Images', '.tiff': 'Images', '.webp': 'Images', '.svg': 'Images',
            
            # Documents
            '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents', '.txt': 'Documents',
            '.rtf': 'Documents', '.odt': 'Documents', '.xlsx': 'Documents', '.pptx': 'Documents',
            '.csv': 'Documents', '.md': 'Documents',
            
            # Audio
            '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio',
            '.aac': 'Audio', '.ogg': 'Audio', '.m4a': 'Audio', '.wma': 'Audio',
            
            # Video
            '.mp4': 'Video', '.avi': 'Video', '.mov': 'Video',
            '.mkv': 'Video', '.wmv': 'Video', '.flv': 'Video', '.webm': 'Video',
            
            # Archives
            '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives',
            '.tar': 'Archives', '.gz': 'Archives', '.bz2': 'Archives',
            
            # Code
            '.py': 'Code', '.java': 'Code', '.cpp': 'Code', '.html': 'Code', '.css': 'Code',
            '.js': 'Code', '.php': 'Code', '.rb': 'Code', '.go': 'Code', '.swift': 'Code',
            '.ts': 'Code', '.sql': 'Code', '.json': 'Code', '.xml': 'Code',
            
            # Executables
            '.exe': 'Executables', '.msi': 'Executables', '.app': 'Executables',
            
            # Fonts
            '.ttf': 'Fonts', '.otf': 'Fonts', '.woff': 'Fonts', '.woff2': 'Fonts',
            
            # Spreadsheets
            '.xls': 'Spreadsheets', '.xlsx': 'Spreadsheets', '.ods': 'Spreadsheets',
            
            # Presentations
            '.ppt': 'Presentations', '.pptx': 'Presentations', '.odp': 'Presentations',
            
            # Ebooks
            '.epub': 'Ebooks', '.mobi': 'Ebooks', '.azw': 'Ebooks',
        }
        
        # Iterate through all files in the directory
        for file_path in dir_path.iterdir():
            if file_path.is_file():
                # Get the file extension
                file_ext = file_path.suffix.lower()

                # Determine the destination folder
                if file_ext in extension_map:
                    dest_folder = dir_path / extension_map[file_ext]
                else:
                    dest_folder = dir_path / 'Other'

                # Create the destination folder if it doesn't exist
                dest_folder.mkdir(exist_ok=True)

                # Move the file to the appropriate folder
                shutil.move(str(file_path), str(dest_folder / file_path.name))
                print(f"Moved {file_path.name} to {dest_folder.name}")

        # Return success message with the actual path used
        return f"Files organized successfully in: {directory}"
        
    except Exception as e:
        print(f"Error in organize_files: {str(e)}")
        raise

if __name__ == "__main__":
    # Prompt the user for the directory path
    directory = input("Enter the path of the directory to organize: ")
    result = organize_files(directory)
    print(result)
