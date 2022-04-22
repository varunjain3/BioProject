import numpy as np

from utility import get_fasta_and_link

def calculate_g4hunter_score(seq):
    
    window_size = len(seq)
    count = 0
    j = 0
    temp = []
    
    while j < (window_size):
        e = seq[j]
        
        temp_count = 1
        
        if e == "G":
            for k in range(j+1, window_size):
                if seq[k] == "G":
                    temp_count += 1
                else:
                    j = k - 1
                    break
            else:
                j = window_size
            temp += [min(temp_count,4) for i in range(temp_count)]
            
            
        elif e == 'C':
            for k in range(j+1, window_size):
                if seq[k] == "C":
                    temp_count += 1
                else:
                    j = k - 1
                    break
            else:
                j = window_size

            temp += [-min(temp_count,4) for i in range(temp_count)]
        else:
            temp += [0]
        j+=1

    return temp


def g4hunter_seq(seq, window_size = 25, threshold = 1.2):
    sequence_hunter = {}
    seq_sqore = calculate_g4hunter_score(seq)

    for i in range(len(seq)-window_size + 1):
        count = sum(seq_sqore[i:i+window_size])/window_size
        if abs(count) >= threshold:
            sequence_hunter[i] = count
    
    # consensus sequence
    
    start = None
    last = None
    consensus_seq = {}

    for start_position in sequence_hunter:
        if start is None:
            start = start_position
            last = start_position
        elif start_position - 1 == last:
            last = start_position
        else:
            new_seq = seq[start:last+window_size]
            new_seq_score = sum(seq_sqore[start:last+window_size])/len(new_seq)
            num_g = numg_calc(new_seq)
            
            consensus_seq[start] = {"sequence": new_seq,
                                    "score": new_seq_score,
                                    "len": len(new_seq),
                                    "num_g":num_g}
            start = start_position
            last = start_position
    

    return consensus_seq



def get_g4hunter_data(NCBI_ID = "NR_152759.1", window_size = 25, threshold = 1.2):

    # make request to the server for an ID
    seq, url = get_fasta_and_link(NCBI_ID)
    results = {"NCBI Reference Number": NCBI_ID,
               "fasta": seq,
               "fasta_url": url}

    sequence_hunter = {}
    seq_sqore = calculate_g4hunter_score(seq)

    for i in range(len(seq)-window_size + 1):
        count = sum(seq_sqore[i:i+window_size])/window_size
        if abs(count) >= threshold:
            sequence_hunter[i] = count
    
    # consensus sequence
    
    start = None
    last = None
    consensus_seq = {}

    for start_position in sequence_hunter:
        if start is None:
            start = start_position
            last = start_position
        elif start_position - 1 == last:
            last = start_position
        else:
            new_seq = seq[start:last+window_size]
            new_seq_score = sum(seq_sqore[start:last+window_size])/len(new_seq)
            
            consensus_seq[start] = {"sequence": new_seq,
                                    "score": new_seq_score,
                                    "len": len(new_seq),}
            start = start_position
            last = start_position
    

    return consensus_seq

def numg_calc(seq):
    numg = None
    score = []
    i = 0

    while i < len(seq):
        if  seq[i] == "G":
            t = 0
            while(seq[t+i]) == "G":
                t += 1

                if t+i>=len(seq):
                    break

            score += [t]
            i += t
        else:
            score += [0]
            i += 1
    
    main_score = score

    for i in range(4,0,-1):
        count = 0
        for j in score:
            if j == i:
                count += 1
        if count >= 4:
            numg = i
            break
        else:
            temp = []
            j = 0
            for j in range(len(main_score)):
                if main_score[j] >= i and i> 1:
                    temp += [i-1]*(main_score[j]//(i-1))

                else:
                    temp += [main_score[j]]

            score = temp
    
    if numg is None:
        return 0
    else:
        return numg



def g4hunter_numgs(NCBI_ID, window_size = 25, threshold = 1.2):
    data = get_g4hunter_data(NCBI_ID, window_size, threshold)
    
    for k,v in data.items():
        data[k]["numg"] = numg_calc(v["sequence"])
    
    return data



if __name__ == "__main__":
    # g4hunter_numgs("NR_152759.1")
    g4hunter_numgs("NR_145130.1")
    print(numg_calc("GTGGGTGTTTGGTGGGCACGAGAGGGGA"))
