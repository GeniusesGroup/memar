/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"time"

	"libgo/authorization"
	"libgo/ganjine"
	"libgo/http"
	"libgo/json"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
)

var getPersonNumberService = service.Service{
	URN:                "urn:giti:sabz.city:service:get-person-number",
	Domain:             DomainName,
	ID:                 2696631725076722377,
	IssueDate:          1603724046,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_Person,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Get Person Number",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"PersonNumber",
	},

	SRPCHandler: GetPersonNumberSRPC,
	ServeHTTP:   GetPersonNumberHTTP,
}

// GetPersonNumberSRPC is sRPC handler of GetPersonNumber service.
func GetPersonNumberSRPC(st protocol.Stream) {
	var res *getPersonNumberRes
	res, err = getPersonNumber(st)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// GetPersonNumberHTTP is HTTP handler of GetPersonNumber service.
func GetPersonNumberHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var res *getPersonNumberRes
	res, err = getPersonNumber(st)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type getPersonNumberRes struct {
	WriteTime        time.Time
	AppInstanceID    [32]byte `json:",string"`
	UserConnectionID [32]byte `json:",string"`
	Number           uint64
	Status           data.PersonNumberStatus
}

func getPersonNumber(st protocol.Stream) (res *getPersonNumberRes, err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}

	// By use st.Connection.UserID just active user can retrieve number that own and don't need to check it anymore!
	var pn = data.PersonNumber{
		PersonID: st.Connection.UserID,
	}
	err = pn.GetLastByPersonID()
	if err != nil {
		if !err.Equal(ganjine.ErrRecordNotFound) {
			err = ErrBadSituation
		}
		return
	}

	res = &getPersonNumberRes{
		WriteTime:     pn.WriteTime,
		AppInstanceID: pn.AppInstanceID,
		// UserConnectionID: pn.UserConnectionID,  TODO::: Due to HTTP use ConnectionID to authenticate connections can't enable it now!!

		Number: pn.Number,
		Status: pn.Status,
	}
	return
}

/*
	Response Encoders & Decoders
*/

func (res *getPersonNumberRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	res.WriteTime = time.Time(syllab.GetInt64(buf, 0))
	copy(res.AppInstanceID[:], buf[8:])
	copy(res.UserConnectionID[:], buf[40:])
	res.Number = syllab.GetUInt64(buf, 72)
	res.Status = data.PersonNumberStatus(syllab.GetUInt8(buf, 80))
	return
}

func (res *getPersonNumberRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.SetInt64(buf, 0, int64(res.WriteTime))
	copy(buf[8:], res.AppInstanceID[:])
	copy(buf[40:], res.UserConnectionID[:])
	syllab.SetUInt64(buf, 72, res.Number)
	syllab.SetUInt8(buf, 80, uint8(res.Status))
	return
}

func (res *getPersonNumberRes) LenOfSyllabStack() uint32 {
	return 81
}

func (res *getPersonNumberRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *getPersonNumberRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *getPersonNumberRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "WriteTime":
			var num int64
			num, err = decoder.DecodeInt64()
			res.WriteTime = time.Time(num)
		case "AppInstanceID":
			err = decoder.DecodeByteArrayAsBase64(res.AppInstanceID[:])
		case "UserConnectionID":
			err = decoder.DecodeByteArrayAsBase64(res.UserConnectionID[:])
		case "Number":
			res.Number, err = decoder.DecodeUInt64()
		case "Status":
			var num uint8
			num, err = decoder.DecodeUInt8()
			res.Status = data.PersonNumberStatus(num)
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (res *getPersonNumberRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"WriteTime":`)
	encoder.EncodeInt64(int64(res.WriteTime))
	encoder.EncodeString(`,"AppInstanceID":"`)
	encoder.EncodeByteSliceAsBase64(res.AppInstanceID[:])
	encoder.EncodeString(`","UserConnectionID":"`)
	encoder.EncodeByteSliceAsBase64(res.UserConnectionID[:])
	encoder.EncodeString(`","Number":`)
	encoder.EncodeUInt64(res.Number)
	encoder.EncodeString(`,"Status":`)
	encoder.EncodeUInt8(uint8(res.Status))
	encoder.EncodeByte('}')
	return encoder.Buf
}

func (res *getPersonNumberRes) LenAsJSON() (ln int) {
	ln = 187
	return
}
