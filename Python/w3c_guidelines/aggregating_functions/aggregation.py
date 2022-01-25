def count_flashes(flashes_lighter, flashes_darker, frame_rate):
    # this may be over-counting slightly
    channel1, channel2 = flashes_lighter[-frame_rate:], flashes_darker[-frame_rate:]
    both_channels = ''
    for i in range(len(channel1)):
        if channel1[i]*channel2[i]:
            both_channels += 'X'
        elif channel1[i]:
            both_channels += '1'
        elif channel2[i]:
            both_channels += '2'
    return (both_channels.count('12')+both_channels.count('21')+both_channels.count('1X')+both_channels.count('X1')+both_channels.count('2X')+both_channels.count('X2'))/2