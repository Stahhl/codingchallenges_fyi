#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int check_characters(const unsigned char *data, int size, char *file_name)
{
    printf("check_characters...\n");
    int char_count = 0;

    while (*data)
    {
        if ((*data & 0xC0) != 0x80) // Count only leading bytes
            char_count++;
        data++;
    }

    printf("%d %s\n", char_count, file_name);

    return EXIT_SUCCESS;
}

int check_words(const unsigned char *data, int size, char *file_name)
{
    printf("check_words...\n");
    int words = 0;
    int in_word = 0; // Flag to track if we are inside a word

    for (int i = 0; i < size; i++)
    {
        if (isspace(data[i]))
        {
            in_word = 0; // Outside a word
        }
        else if (!in_word)
        {
            in_word = 1; // Entering a new word
            words++;
        }
    }

    printf("%d %s\n", words, file_name);

    return EXIT_SUCCESS;
}

int check_lines(const unsigned char *data, int size, char *file_name)
{
    printf("check_lines...\n");

    int lines = 0;
    for (int i = 0; i < size; i++)
    {
        if (data[i] == '\n')
        { // Newline character found
            lines++;
        }
    }
    printf("%d %s\n", lines, file_name);
    return EXIT_SUCCESS;
}

char *get_file_name(int argc, char *argv[])
{
    char *file_name = "";
    // Iterate through each argument (starting from 1 to skip the program name)
    for (int i = 1; i < argc; ++i)
    {
        // Check if the argument doesn't start with '-' and isn't empty
        if (argv[i][0] != '-' && strlen(argv[i]) > 0)
        {
            file_name = argv[i]; // Return the first non-flag argument (file name)
        }
    }

    printf("get_file_name: %s\n", file_name);
    return file_name; // Return NULL if no file name is found
}

/*
    "" => "clw"
    "foo" => "clw"
    "-c" => "c"
    "-c foo" => "c"
    "-cl" => "cl"
    "-cl foo" => "foo"
    "-c -l" => "cl"
    "-c -l foo" => "cl"
*/
char *get_flags(int argc, char *argv[])
{
    static char result[4] = ""; // Buffer to store the result ("clw", "c", etc.)
    int flags_set = 0;          // Track if any flags are set

    for (int i = 1; i < argc; ++i)
    {
        char *arg = argv[i];

        // Check if the argument is a flag (starts with '-')
        if (arg[0] == '-')
        {
            // Add 'c', 'l', or 'w' to result based on the flags
            for (int j = 1; arg[j] != '\0'; ++j)
            {
                result[flags_set++] = arg[j];
            }
        }
    }

    // If no non-flag argument is found, return the default "clw"
    if (flags_set == 0)
    {
        strcpy(result, "clw");
    }

    printf("get_flags: %s\n", result);
    return result;
}

unsigned char *get_data_from_stdin(int *size) {
    size_t INITIAL_BUFFER_SIZE = 1024;
    size_t buffer_size = INITIAL_BUFFER_SIZE;
    size_t total_bytes = 0;
    size_t bytes_read = 0;
    unsigned char temp_buffer[INITIAL_BUFFER_SIZE];
    
    // Allocate initial buffer
    unsigned char *buffer = (unsigned char*)malloc(buffer_size);
    if (buffer == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }
    
    // Read data from stdin in chunks
    while ((bytes_read = fread(temp_buffer, 1, INITIAL_BUFFER_SIZE, stdin)) > 0) {
        // Check if we need to resize the buffer
        if (total_bytes + bytes_read > buffer_size) {
            buffer_size *= 2;
            unsigned char* new_buffer = (unsigned char*)realloc(buffer, buffer_size);
            if (new_buffer == NULL) {
                fprintf(stderr, "Memory reallocation failed\n");
                free(buffer);
                return NULL;
            }
            buffer = new_buffer;
        }
        
        // Copy the temp buffer to the main buffer
        memcpy(buffer + total_bytes, temp_buffer, bytes_read);
        total_bytes += bytes_read;
    }
    
    // Update the size parameter with total bytes read
    *size = (int)total_bytes;
    
    // If we read 0 bytes, return an empty buffer
    if (total_bytes == 0) {
        return buffer;
    }
    
    // Resize buffer to exact size if needed
    if (total_bytes < buffer_size) {
        unsigned char *final_buffer = (unsigned char*)realloc(buffer, total_bytes);
        if (final_buffer != NULL) {
            buffer = final_buffer;
        }
        // If realloc fails, we keep the original buffer which is still valid
    }
    
    return buffer;
}

unsigned char *get_data_from_file(char *file_name, int *size)
{
    printf("get_data_from_file...\n");

    FILE *file = fopen(file_name, "rb");
    if (!file)
    {
        perror("Failed to open file");
        return NULL;
    }

    // Get file size
    fseek(file, 0, SEEK_END);
    *size = ftell(file);
    rewind(file);

    // Allocate memory
    unsigned char *buffer = malloc(*size);
    if (!buffer)
    {
        perror("Memory allocation failed");
        fclose(file);
        return NULL;
    }

    // Read file into buffer
    fread(buffer, 1, *size, file);
    fclose(file);

    return buffer;
}

unsigned char *get_data(char *file_name, int *size)
{
    if (file_name == NULL || file_name[0] == '\0')
    {
        printf("stdin...\n");
        return get_data_from_stdin(size);
    }

    return get_data_from_file(file_name, size);
}

int main(int argc, char *argv[])
{
    for (int i = 0; i < argc; i++)
    {
        printf("%d: %s\n", i, argv[i]);
    }

    int size;
    char *file_name = get_file_name(argc, argv);
    char *flags = get_flags(argc, argv);
    unsigned char *data = get_data(file_name, &size);

    if (strchr(flags, 'c') != NULL)
    {
        printf("check_bytes...\n");
        printf("%d %s\n", size, file_name);
    }

    if (strchr(flags, 'l') != NULL)
    {
        if (check_lines(data, size, file_name) != EXIT_SUCCESS)
        {
            return EXIT_FAILURE;
        }
    }

    if (strchr(flags, 'w') != NULL)
    {
        if (check_words(data, size, file_name) != EXIT_SUCCESS)
        {
            return EXIT_FAILURE;
        }
    }

    if (strchr(flags, 'm') != NULL)
    {
        if (check_characters(data, size, file_name) != EXIT_SUCCESS)
        {
            return EXIT_FAILURE;
        }
    }

    free(data);
    return EXIT_SUCCESS;
}
