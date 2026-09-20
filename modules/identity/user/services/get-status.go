/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"libgo/authorization"
	"libgo/ganjine"
	"libgo/http"
	"libgo/json"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
)

var getPersonNumberStatusService = service.Service{
	URN:                "urn:giti:sabz.city:service:get-person-number-status",
	Domain:             DomainName,
	ID:                 10007602070941096790,
	IssueDate:          1602742728,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "GetPersonNumberStatus",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"PersonNumber",
	},

	SRPCHandler: GetPersonNumberStatusSRPC,
	ServeHTTP:   GetPersonNumberStatusHTTP,
}

// GetPersonNumberStatusSRPC is sRPC handler of GetPersonNumberStatus service.
func GetPersonNumberStatusSRPC(st protocol.Stream) {
	var req = &getPersonNumberStatusReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *getPersonNumberStatusRes
	res, err = getPersonNumberStatus(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// GetPersonNumberStatusHTTP is HTTP handler of GetPersonNumberStatus service.
func GetPersonNumberStatusHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &getPersonNumberStatusReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *getPersonNumberStatusRes
	res, err = getPersonNumberStatus(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type getPersonNumberStatusReq struct {
	CaptchaID   [16]byte `json:",string"`
	PhoneNumber uint64
}

type getPersonNumberStatusRes struct {
	PersonID [32]byte `json:",string"` // UUID of registered user
	Status   data.PersonNumberStatus
}

func getPersonNumberStatus(st protocol.Stream, req *getPersonNumberStatusReq) (res *getPersonNumberStatusRes, err protocol.Error) {
	if st.Connection.UserType == protocol.UserType_Unset {
		// Prevent DDos attack by do some easy process for user e.g. captcha is not good way!
		err = phraseCaptchas.Check(req.CaptchaID)
		if err != nil {
			return
		}
	}

	var pn = data.PersonNumber{
		Number: req.PhoneNumber,
	}
	err = pn.GetLastByNumber()
	if err != nil {
		if err.Equal(ganjine.ErrRecordNotFound) {
			err = nil
		} else {
			err = ErrBadSituation
			return
		}
	}

	res = &getPersonNumberStatusRes{
		PersonID: pn.PersonID,
		Status:   pn.Status,
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *getPersonNumberStatusReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.CaptchaID[:], buf[0:])
	req.PhoneNumber = syllab.GetUInt64(buf, 0)
	return
}

func (req *getPersonNumberStatusReq) LenOfSyllabStack() uint32 {
	return 24
}

func (req *getPersonNumberStatusReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "CaptchaID":
			err = decoder.DecodeByteArrayAsBase64(req.CaptchaID[:])
		case "PhoneNumber":
			req.PhoneNumber, err = decoder.DecodeUInt64()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

/*
	Response Encoders & Decoders
*/

func (res *getPersonNumberStatusRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.SetUInt8(buf, 0, uint8(res.Status))
}

func (res *getPersonNumberStatusRes) LenOfSyllabStack() uint32 {
	return 1
}

func (res *getPersonNumberStatusRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *getPersonNumberStatusRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *getPersonNumberStatusRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"PersonID":"`)
	encoder.EncodeByteSliceAsBase64(res.PersonID[:])
	encoder.EncodeString(`","Status":`)
	encoder.EncodeUInt8(uint8(res.Status))
	encoder.EncodeByte('}')
	return encoder.Buf
}

func (res *getPersonNumberStatusRes) LenAsJSON() (ln int) {
	ln = 71
	return
}
