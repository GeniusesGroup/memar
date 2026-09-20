/* For license and copyright information please see the LEGAL file in the code repository */

package pa

import (
	"libgo/authorization"
	"libgo/http"
	"libgo/json"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
)

var getPersonStatusService = service.Service{
	URN:                "urn:giti:sabz.city:service:get-person-status",
	Domain:             DomainName,
	ID:                 18258809357264053508,
	IssueDate:          1604744631,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All ^ protocol.UserType_Unset, // TODO::: allow to user circles get person status??
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Get Person Status",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"PersonAuthentication",
	},

	SRPCHandler: GetPersonStatusSRPC,
	ServeHTTP:   GetPersonStatusHTTP,
}

// GetPersonStatusSRPC is sRPC handler of GetPersonStatus service.
func GetPersonStatusSRPC(st protocol.Stream) {
	var req = &getPersonStatusReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *getPersonStatusRes
	res, err = getPersonStatus(st, req, false)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// GetPersonStatusHTTP is HTTP handler of GetPersonStatus service.
func GetPersonStatusHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &getPersonStatusReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *getPersonStatusRes
	res, err = getPersonStatus(st, req, false)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type getPersonStatusReq struct {
	PersonID [32]byte `json:",string"`
}

type getPersonStatusRes struct {
	AppInstanceID    [32]byte `json:",string"`
	UserConnectionID [32]byte `json:",string"`

	ReferentPersonID [32]byte `json:",string"`
	Status           data.PersonAuthenticationStatus
}

func getPersonStatus(st protocol.Stream, req *getPersonStatusReq, unsafe bool) (res *getPersonStatusRes, err protocol.Error) {
	if !unsafe {
		err = st.Authorize()
		if err != nil {
			return
		}
	}

	var pa = data.PersonAuthentication{
		PersonID: req.PersonID,
	}
	err = pa.GetLastByPersonID()
	if err != nil {
		return
	}

	res = &getPersonStatusRes{
		AppInstanceID: pa.AppInstanceID,
		// UserConnectionID: pa.UserConnectionID, TODO::: Due to HTTP use ConnectionID to authenticate connections can't enable it now!!
		ReferentPersonID: pa.ReferentPersonID,
		Status:           pa.Status,
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *getPersonStatusReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.PersonID[:], buf[0:])
	return
}

func (req *getPersonStatusReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.PersonID[:])
	return
}

func (req *getPersonStatusReq) LenOfSyllabStack() uint32 {
	return 32
}

func (req *getPersonStatusReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *getPersonStatusReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *getPersonStatusReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "PersonID":
			err = decoder.DecodeByteArrayAsBase64(req.PersonID[:])
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *getPersonStatusReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"PersonID":"`)
	encoder.EncodeByteSliceAsBase64(req.PersonID[:])

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (req *getPersonStatusReq) LenAsJSON() (ln int) {
	ln = 58
	return
}

/*
	Response Encoders & Decoders
*/

func (res *getPersonStatusRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(res.AppInstanceID[:], buf[0:])
	copy(res.UserConnectionID[:], buf[32:])
	copy(res.ReferentPersonID[:], buf[64:])
	res.Status = data.PersonAuthenticationStatus(syllab.GetUInt8(buf, 96))
	return
}

func (res *getPersonStatusRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], res.AppInstanceID[:])
	copy(buf[32:], res.UserConnectionID[:])
	copy(buf[64:], res.ReferentPersonID[:])
	syllab.SetUInt8(buf, 96, uint8(res.Status))
	return
}

func (res *getPersonStatusRes) LenOfSyllabStack() uint32 {
	return 97
}

func (res *getPersonStatusRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *getPersonStatusRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *getPersonStatusRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "AppInstanceID":
			err = decoder.DecodeByteArrayAsBase64(res.AppInstanceID[:])
		case "UserConnectionID":
			err = decoder.DecodeByteArrayAsBase64(res.UserConnectionID[:])
		case "ReferentPersonID":
			err = decoder.DecodeByteArrayAsBase64(res.ReferentPersonID[:])
		case "Status":
			var num uint8
			num, err = decoder.DecodeUInt8()
			res.Status = data.PersonAuthenticationStatus(num)
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (res *getPersonStatusRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"AppInstanceID":"`)
	encoder.EncodeByteSliceAsBase64(res.AppInstanceID[:])
	encoder.EncodeString(`","UserConnectionID":"`)
	encoder.EncodeByteSliceAsBase64(res.UserConnectionID[:])
	encoder.EncodeString(`","ReferentPersonID":"`)
	encoder.EncodeByteSliceAsBase64(res.ReferentPersonID[:])
	encoder.EncodeString(`","Status":`)
	encoder.EncodeUInt8(uint8(res.Status))
	encoder.EncodeByte('}')
	return encoder.Buf
}

func (res *getPersonStatusRes) LenAsJSON() (ln int) {
	ln = 206
	return
}
