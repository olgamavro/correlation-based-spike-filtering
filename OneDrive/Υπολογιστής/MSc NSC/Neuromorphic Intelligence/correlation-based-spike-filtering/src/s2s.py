import pyaudio
from speech2spikes import S2S
import keyboard
import time
import torch
from scipy.io.wavfile import read
import wave
from scipy.stats import zscore

import numpy as np

def record_audio(Output_Filename = "Recorded.wav", CHUNKSIZE = 1024):
    
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    
    # initialize portaudio
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=CHUNKSIZE)

    
    frames = []
    print("Press SPACE to start recording")
    keyboard.wait('space')
    print("Recording... Press SPACE to stop.")
    time.sleep(0.2)
    
    while True:
        try:
            data = stream.read(CHUNKSIZE)  
            frames.append(data)
        except KeyboardInterrupt:
            break
        if keyboard.is_pressed('space'):
            print("stopping recording") 
            time.sleep(0.2)
            break   

    # close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(Output_Filename, 'wb')  
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    
def wav2batch(filename="hey.wav"):
    sample_rate, audio = read(filename)

    print(filename, " : sample rate ", sample_rate, " | duration ", len(audio) / sample_rate, "s")

    audio = zscore(audio.astype("float32"))

    waveform = torch.tensor(audio)

    if waveform.ndim == 1:
        waveform = waveform.unsqueeze(0)
        
    return [(waveform, torch.tensor([t / sample_rate for t in range(len(audio))]))] 

def batch2spikes(batch, quiz=False):
    
    windows_per_pattern = 11
    repetitions = 1
    
    s2s = S2S()
    s2s.configure(hop_length = 100, win_length = 200, n_mels = 15)

    spike_trains = s2s(batch)
    spikes_per_window = np.abs(np.array(spike_trains[0][0][0][1:14,:], dtype=int))

    if quiz:
        
        return np.array([np.repeat(spikes_per_window[:, i:i+windows_per_pattern].reshape(1, -1)[0], repetitions) for i in range(np.shape(spikes_per_window)[1] - windows_per_pattern)]).reshape(1, -1)
    else:
    
        return np.array([np.repeat(spikes_per_window[:, i:i+windows_per_pattern].reshape(1, -1)[0], repetitions) for i in range(np.shape(spikes_per_window)[1] - windows_per_pattern)])



def crop_spikes(spikes, N_POPULATION=4):
    return spikes[0:np.shape(spikes)[0] - np.shape(spikes)[0] % N_POPULATION**2]

def spikes2wordquiz(batch_array):
    # Find the maximum total elements in any pattern
    max_len = max(np.size(word) for word in batch_array)
    
    padded_list = []
    for word in batch_array:
        flat_word = np.ravel(word)
        pad_amount = max_len - len(flat_word)
        
        # Pad 0 elements on the left, and pad_amount elements on the right
        padded_word = np.pad(flat_word, (0, pad_amount), mode='constant', constant_values=0)
        padded_list.append(padded_word)
        
    raw_quiz = np.array(padded_list)

    return raw_quiz

def main(word_quiz = False):
    
    if word_quiz:
        batch1 = wav2batch("audio/one.wav")
        batch2 = wav2batch("audio/two.wav")
        batch3 = wav2batch("audio/three.wav")
        batch4 = wav2batch("audio/four.wav")
        
        input_spikes = spikes2wordquiz([batch2spikes(batch1, word_quiz), batch2spikes(batch2, word_quiz), batch2spikes(batch3, word_quiz), batch2spikes(batch4, word_quiz)])

        np.savetxt("quiz_input.txt", input_spikes)
        
    else:
        batch = wav2batch("audio/two.wav")
        input_spikes = batch2spikes(batch)
    
        np.savetxt("spikes.txt", crop_spikes(input_spikes))

main()
    