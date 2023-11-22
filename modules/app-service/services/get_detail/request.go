/* For license and copyright information please see the LEGAL file in the code repository */

package gds

import (
	"memar/json"
	"memar/protocol"
	"memar/syllab"
)

type Request struct {
	ServiceID  uint64
	ServiceURI string
}

func (req *Request) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	req.ServiceID = syllab.GetUInt64(buf, 0)
	req.ServiceURI = syllab.UnsafeGetString(buf, 8)
	return
}

func (req *Request) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.SetUInt64(buf, 0, req.ServiceID)
	syllab.SetString(buf, req.ServiceURI, 8, heapIndex)
	return
}

func (req *Request) LenOfSyllabStack() uint32 {
	return 16
}

func (req *Request) LenOfSyllabHeap() (ln uint32) {
	ln += uint32(len(req.ServiceURI))
	return
}

func (req *Request) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *Request) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "ServiceID":
			req.ServiceID, err = decoder.DecodeUInt64()
		case "ServiceURI":
			req.ServiceURI, err = decoder.DecodeString()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *Request) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"ServiceID":`)
	encoder.EncodeUInt64(req.ServiceID)

	encoder.EncodeString(`,"ServiceURI":"`)
	encoder.EncodeString(req.ServiceURI)

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (req *Request) LenAsJSON() (ln int) {
	ln = 60
	ln += len(req.ServiceURI)
	return
}
