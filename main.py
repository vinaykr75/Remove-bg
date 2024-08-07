from rembg import remove
from PIL import Image
import io
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters,CallbackContext
from keep_alive import keep_alive

keep_alive()

TOKEN = '7065303069:AAEzqfj_H_pZOrvnqoOsWAjC0AYdk8NCH7Q'

async def start(update: Update, context: CallbackContext) -> None:
   await update.message.reply_text('Hi! Send me a photo and I will remove the background for you.')

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send me a photo and I will remove the background.')

async def remove_background(update: Update, context: CallbackContext) -> None:
   
 waiting_message = await update.message.reply_text('Processing your image, please wait...')
   
 try:  
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    photo_path = await photo_file.download_to_drive()

    # Open the photo and remove the background
    with open(photo_path, 'rb') as input_file:
        input_image = input_file.read()

    output_image = remove(input_image)

    # Save the output image
    output_path = 'output.png'
    img = Image.open(io.BytesIO(output_image)).convert("RGBA")
    img.save(output_path, format='PNG')
    
    # Send the output image back to the user
    with open(output_path, 'rb') as output_file:
        await update.message.reply_document(document=output_file)
 
 except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

 finally:
        # Cleanup
        if os.path.exists(photo_path):
            os.remove(photo_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        # Delete the waiting message
        await waiting_message.delete()

if __name__ == '__main__':
    print('Starting...')
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler('start',start))
    app.add_handler(CommandHandler('help',help_command))

    app.add_handler(MessageHandler(filters.PHOTO,remove_background))
    
    app.run_polling(poll_interval=3)
