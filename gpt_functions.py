import os

from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()
openAI_key = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=openAI_key)


def create_assistant(assistant_name, my_instruction):
    """
        This function is used to create an assistant in OpenAI.
        :return: assistant.id
    """
    my_assistant = client.beta.assistants.create(
        name=assistant_name,
        description="Virtual assistant to help customers to order food for a restaurant",
        instructions=my_instruction,
        model="gpt-4o",
    )

    return my_assistant.id


def show_assistants():
    """
        Show the list of assistants created using the OpenAI key.
        :return: List of assistants
    """
    my_updated_assistant = client.beta.assistants.list()
    return my_updated_assistant


def updateAssistantInstruction(assistant_id, new_instruction):
    """
        Update the instructions of an assistant.
        :return: Updated assistant object
    """
    my_updated_assistant = client.beta.assistants.update(
        assistant_id, instructions=new_instruction
    )
    return my_updated_assistant


# ====================================================
# OpenAI Assistant tools: File Search and Vector Store
# ====================================================
def saveFile_intoOpenAI(file_location):
    """
    This function is used to upload a file into OpenAI
    :return: file.id
    """
    file = client.files.create(
        file=open(file_location, "rb"),
        purpose='assistants'
    )
    return file.id


def deleteFile(file_id):
    """
        Delete a file from OpenAI.
        :return: Deletion status
    """
    file_deletion_status = client.files.delete(file_id=file_id)

    return file_deletion_status


def create_vector_store(store_name):
    """
        Create a vector store for file searching.
        :return: Vector store ID
    """
    vector_store = client.beta.vector_stores.create(name=store_name)
    return vector_store.id


def upload_file_into_vector_store(vector_store_id, file_ids):
    """
        Upload a file or batch of files to the vector store.
        :return: Status of file upload
    """

    file_batch = client.beta.vector_stores.file_batches.create(
        vector_store_id=vector_store_id, file_ids=file_ids
    )

    # Print the status and the file counts of the batch to see the result of this operation.
    print(file_batch.status)
    print(file_batch.file_counts)

    print("Done Uploading")
    return file_batch.status


def updateAssistantVectorDB(assistant_id, vector_store_id):
    """
        Connect a vector store with the assistant.
        :return: None
    """
    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    )
    print("vector store connected with Assistant")


def delete_vector_store_file(vector_store_id, file_id):
    """
        Delete a file from the vector store.
        :return: None
    """
    deleted_vector_store_file = client.beta.vector_stores.files.delete(
        vector_store_id=vector_store_id,
        file_id=file_id
    )
    print(deleted_vector_store_file)


def createThread(prompt):
    """
        Create a thread to initiate interaction with an assistant.
        :return: Thread ID
    """
    messages = [{"role": "user", "content": prompt}]
    thread = client.beta.threads.create(messages=messages)
    return thread.id


# Run the Assistance
def runAssistant(thread_id, assistant_id):
    """
        Trigger the assistant to run on a thread. This will start the conversation.
        :return: Run details
    """
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    return run


def sendNewMessage(thread_id, message):
    """
        Send a new message in an existing thread.
        :return: None
        """
    thread_message = client.beta.threads.messages.create(
        thread_id, role="user", content=message
    )


def retrieveResponse(thread_id):
    """
        Retrieve the response from an existing thread.
        :return: Assistant's response content
    """
    thread_messages = client.beta.threads.messages.list(thread_id)
    list_messages = thread_messages.data
    assistant_message = list_messages[0]
    message_text = assistant_message.content[0].text.value
    return message_text


def checkRunStatus(thread_id, run_id):
    """
    Check the status of a running thread.
    :return: Run status
    """
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id, run_id=run_id
    )
    return run
# ===========================================================
# End of OpenAI Assistant tools: File Search and Vector Store
# ===========================================================
