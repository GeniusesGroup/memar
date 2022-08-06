/* For license and copyright information please see LEGAL file in repository */

package services

import (
	"github.com/GeniusesGroup/libgo/json"
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/syllab"
)

/*
	Service request structure
*/

type GetRequest struct {
	quiddityID [16]byte `json:"QuiddityID,string"`
}

func (req *GetRequest) QuiddityID() [16]byte       { return req.quiddityID }
func (req *GetRequest) SetQuiddityID(qid [16]byte) { req.quiddityID = qid }

// Syllab codec
func (req *GetRequest) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.ID[:], buf[0:])
	req.Language = protocol.Language(syllab.GetUInt32(buf, 32))
	return
}
func (req *GetRequest) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.ID[:])
	syllab.SetUInt32(buf, 32, uint32(req.Language))
	return
}
func (req *GetRequest) LenOfSyllabStack() uint32 {
	return 36
}
func (req *GetRequest) LenOfSyllabHeap() (ln uint32) {
	return
}
func (req *GetRequest) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

// JSON codec
func (req *GetRequest) FromJSON(payload []byte) (err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "QuiddityID":
			err = decoder.DecodeByteArrayAsBase64(req.quiddityID[:])
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}
func (req *GetRequest) ToJSON(payload []byte) []byte {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"QuiddityID":"`)
	encoder.EncodeByteSliceAsBase64(req.quiddityID[:])
	encoder.EncodeByte('}')
	return encoder.Buf
}
func (req *GetRequest) LenAsJSON() (ln int) {
	ln = 50
	return
}

/*
	Service request as Syllab
*/

type getRequest_Syllab []byte

func (req *getRequest_Syllab) QuiddityID() (qid [16]byte) {
	syllab.GetFixedByteArray(*req, 0, qid[:])
	return
}
