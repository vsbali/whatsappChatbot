# Stadard librarires
import time
import pandas as pd
import xlrd
import openpyxl

# project modules
from whatsaAppModules import *

# import configs
from config import *

# Driver intialization
# driver = webdriver.Firefox()




def main():
    strart_time = time.time()

    # Read message file
    message = open(messageFile, 'r').read()

    # Read Client data
    df = pd.read_excel(xl_file, sheet_name=xl_sheet)
    # Create Result file
    dfResult = df
    dfResult['status'] = ''

    # WhatsApp authentication
    authenticate()

    try:
        for i in range(df.name.count()):
            time.sleep(2)
            openClientChat(whatsapp_web_url + '91' + str(df.mobile_no[i]))
            sendMessage(str(df.name[i]) + '\n' + message)
            # time.sleep(2)
            if not attachmentFilePath == 'No':
                sendAttachment(attachmentFilePath)
            time.sleep(2)
            closeClientChat()
            # Sent status update
            dfResult['status'][i] = 'sent'

        # Write results to file
        dfResult.to_excel(xl_sentResult)

        '''
        for contact in contacts:
            time.sleep(2)
            openClientChat(whatsapp_web_url + contact)
            sendMessage(whatsappMessage)
            #time.sleep(2)
            sendAttachment(file_path)
            time.sleep(2)
            closeClientChat()
        '''
        print("Time taken to complete script : {}".format(time.time() - strart_time))
    except:
        print("Time taken to complete script : {}".format(time.time() - strart_time))
        dfResult.to_excel(xl_sentResult)
        raise


if __name__ == "__main__":
    main()