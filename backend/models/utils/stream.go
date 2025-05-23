package utils

import "bytes"

func IsImage(data []byte) bool {
	//JPEG
	if bytes.HasPrefix(data, []byte{0xFF, 0xD8}) {
		return true
	}
	//PNG
	if bytes.HasPrefix(data, []byte{0x89, 0x50, 0x4E, 0x47}) {
		return true
	}
	return false
}

func IsAudio(data []byte) bool {
	// WAV
	if bytes.HasPrefix(data, []byte{0x43}) {
		return data[2] == 0x81
	}
	return false
}
