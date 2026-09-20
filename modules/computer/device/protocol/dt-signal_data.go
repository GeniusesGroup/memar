/* For license and copyright information please see the LEGAL file in the code repository */

package device_p

type Field_SignalData interface {
	// SignalData or value is data that SendFrom(output)||ReceivedTo(input) devices.
	// It not use to transfer huge data format like audio or video.
	// Related modules MUST use other mechanism on content and object module.
	SignalData() []byte
}

type SignalData []byte
