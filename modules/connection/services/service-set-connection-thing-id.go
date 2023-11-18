/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"memar/authorization"
	er "memar/error"
	"memar/http"
	"memar/json"
	lang "memar/language"
	"memar/srpc"
	"memar/syllab"
	"memar/protocol"
	"memar/service"
)

var setConnectionThingIDService = service.Service{
	URN:                "domain/achaemenid.protocol.service; name=set-connection-thing-id",
	Domain:             DomainName,
	ID:                 3530667464632943931,
	IssueDate:          1604844006,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PerpetualBeta,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDCreate,
		UserType: protocol.UserType_All,
	},

	Detail: map[protocol.LanguageID]service.ServiceDetail{
		protocol.LanguageEnglish: {
			Name:        "Set Connection Thing ID",
			Description: "This service just valid until TCP||UDP support",
			TAGS:        []string{"Temporary"},
		},
	},

	SRPCHandler: SetConnectionThingIDSRPC,
	ServeHTTP: SetConnectionThingIDHTTP,
}

// SetConnectionThingIDSRPC is sRPC handler of SetConnectionThingID service.
func SetConnectionThingIDSRPC(st protocol.Stream) {
	var req = &setConnectionThingIDReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	err = setConnectionThingID(st, req)
	// Check if any error occur in bussiness logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength)
}

// SetConnectionThingIDHTTP is HTTP handler of SetConnectionThingID service.
func SetConnectionThingIDHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &setConnectionThingIDReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	err = setConnectionThingID(st, req)
	// Check if any error occur in bussiness logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
}

type setConnectionThingIDReq struct {
	ThingID [32]byte `json:",string"`
}

func setConnectionThingID(st protocol.Stream, req *setConnectionThingIDReq) (err protocol.Error) {
	if st.Connection.ThingID == [32]byte{} {
		st.Connection.ThingID = req.ThingID
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *setConnectionThingIDReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.ThingID[:], buf[0:])
	return
}

func (req *setConnectionThingIDReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32)
	copy(buf[0:], req.ThingID[:])
	return
}

func (req *setConnectionThingIDReq) LenOfSyllabStack() uint32 {
	return 32
}

func (req *setConnectionThingIDReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *setConnectionThingIDReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *setConnectionThingIDReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "ThingID":
			err = decoder.DecodeByteArrayAsBase64(req.ThingID[:])
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *setConnectionThingIDReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"ThingID":"`)
	encoder.EncodeByteSliceAsBase64(req.ThingID[:])

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (req *setConnectionThingIDReq) LenAsJSON() (ln int) {
	ln = 57
	return
}
