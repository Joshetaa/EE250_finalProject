## IMPORTS
import pandas as pd
import speech_recognition as sr
import sys

## FACE DETECTION OUTPUT (tensorflow + CV)






## SPEECH TO TEXT CONVERSION
# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Reading Audio file as source
# listening the audio file and store in audio_text variable

with sr.AudioFile('Audio_data/test_angry.wav') as source:
    
    audio_text = r.listen(source)
    
# recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        
        # using google speech recognition
        text = r.recognize_google(audio_text)
        print('\nConverting audio transcripts into text ...')
        print(text)
     
    except:
         print('Sorry.. run again...')


## PROCESS TEXT INTO APPROPRIATE STRUCTURE (LIST OF WORDS)
text_list = text.split()
print("\nSplit text is: ", text_list)


## FINDING TRIGGER WORDS
# Get dataset 
filepath = "NRC_data/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"], skiprows=45, sep='\t', keep_default_na=False)
emolex_words = emolex_df.pivot(index='word', columns='emotion', values='association').reset_index()

# inits
sadness_words = emolex_words[emolex_words.sadness == 1].word.values
anger_words = emolex_words[emolex_words.anger == 1].word.values
joy_words = emolex_words[emolex_words.joy == 1].word.values
triggerWords = []


# get emotion from command line
emotion = sys.argv[1] # out put form caleb's script 
if emotion == "Anger":
    word_base = anger_words
elif emotion == "Sad":
    word_base = sadness_words
elif emotion == "Happy":
    word_base = joy_words

# check sentence
for word in text_list:
    if word in word_base:
        triggerWords.append(str(word))


print("\nTrigger words for {}: ".format(emotion), triggerWords)

