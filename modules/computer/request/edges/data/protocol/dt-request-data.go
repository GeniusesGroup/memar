/* For license and copyright information please see the LEGAL file in the code repository */

package request_data_p

type Field_RequestData interface {
	RequestData() RequestData
}

// RequestData will decode by service request structure and compress type.
type RequestData []byte
