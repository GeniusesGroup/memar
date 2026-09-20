/* For license and copyright information please see the LEGAL file in the code repository */

package quiddity

import (
	"strconv"

	"libgo/authorization"
	"libgo/http"
	"libgo/json"
	lang "libgo/language"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
)

var getQuiddityLanguagesService = service.Service{
	URN:                "urn:giti:sabz.city:service:get-quiddity-languages",
	Domain:             DomainName,
	ID:                 18295424837419209043,
	IssueDate:          1605106959,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Get Quiddity Languages",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"Quiddity",
	},

	SRPCHandler: GetQuiddityLanguagesSRPC,
	ServeHTTP:   GetQuiddityLanguagesHTTP,
}

// GetQuiddityLanguagesSRPC is sRPC handler of GetQuiddityLanguages service.
func GetQuiddityLanguagesSRPC(st protocol.Stream) {
	var req = &getQuiddityLanguagesReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *getQuiddityLanguagesRes
	res, err = getQuiddityLanguages(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// GetQuiddityLanguagesHTTP is HTTP handler of GetQuiddityLanguages service.
func GetQuiddityLanguagesHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &getQuiddityLanguagesReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *getQuiddityLanguagesRes
	res, err = getQuiddityLanguages(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type getQuiddityLanguagesReq struct {
	ID [32]byte `json:",string"`
}

type getQuiddityLanguagesRes struct {
	Languages []protocol.Language
}

func getQuiddityLanguages(st protocol.Stream, req *getQuiddityLanguagesReq) (res *getQuiddityLanguagesRes, err protocol.Error) {
	var w = data.Quiddity{
		ID: req.ID,
	}
	res = &getQuiddityLanguagesRes{}
	res.Languages, err = w.FindLanguagesByID(0, 100)
	return
}

/*
	Request Encoders & Decoders
*/

func (req *getQuiddityLanguagesReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.ID[:], buf[0:])
	return
}

func (req *getQuiddityLanguagesReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.ID[:])
	return
}

func (req *getQuiddityLanguagesReq) LenOfSyllabStack() uint32 {
	return 32
}

func (req *getQuiddityLanguagesReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *getQuiddityLanguagesReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *getQuiddityLanguagesReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "ID":
			err = decoder.DecodeByteArrayAsBase64(req.ID[:])
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *getQuiddityLanguagesReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"ID":"`)
	encoder.EncodeByteSliceAsBase64(req.ID[:])

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (req *getQuiddityLanguagesReq) LenAsJSON() (ln int) {
	ln = 52
	return
}

/*
	Response Encoders & Decoders
*/

func (res *getQuiddityLanguagesRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	var add uint32 = syllab.GetUInt32(buf, 0)
	var ln uint32 = syllab.GetUInt32(buf, 0+4)
	res.Languages = lang.UnsafeByteSliceToLanguagesSlice(buf[add : add+(ln*4)])
	return
}

func (res *getQuiddityLanguagesRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	var ln = uint32(len(res.Languages))
	syllab.SetUInt32(buf, 0, heapIndex)
	syllab.SetUInt32(buf, 0+4, ln)
	copy(buf[heapIndex:], lang.UnsafeLanguagesSliceToByteSlice(res.Languages))
	// heapIndex = heapIndex + (ln * 4)
	return
}

func (res *getQuiddityLanguagesRes) LenOfSyllabStack() uint32 {
	return 8
}

func (res *getQuiddityLanguagesRes) LenOfSyllabHeap() (ln uint32) {
	ln += uint32(len(res.Languages) * 4)
	return
}

func (res *getQuiddityLanguagesRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *getQuiddityLanguagesRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "Languages":
			var num uint32
			res.Languages = make([]protocol.LanguageID, 0, 8) // TODO::: Is cap efficient enough?
			for !decoder.CheckToken(']') {
				num, err = decoder.DecodeUInt32()
				if err != nil {
					return
				}
				res.Languages = append(res.Languages, protocol.Language(num))
				decoder.Offset(1)
			}
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (res *getQuiddityLanguagesRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"Languages":[`)
	var ln = len(res.Languages)
	for i := 0; i < ln; i++ {
		encoder.Buf = strconv.AppendUint(encoder.Buf, uint64(res.Languages[i]), 10)
		encoder.Buf = append(encoder.Buf, ',')
	}
	encoder.RemoveTrailingComma()

	encoder.EncodeString(`]}`)
}

func (res *getQuiddityLanguagesRes) LenAsJSON() (ln int) {
	ln = (len(res.Languages) * 11)
	ln += 16
	return
}
