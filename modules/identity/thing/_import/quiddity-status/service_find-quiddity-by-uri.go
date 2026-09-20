/* For license and copyright information please see the LEGAL file in the code repository */

package quiddity

import (
	"libgo/authorization"
	"libgo/http"
	"libgo/json"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
)

var findQuiddityByURIService = service.Service{
	URN:                "urn:giti:sabz.city:service:find-quiddity-by-uri",
	Domain:             DomainName,
	ID:                 16220032743128053382,
	IssueDate:          1605026726,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Find Quiddity By URI",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"Quiddity",
	},

	SRPCHandler: FindQuiddityByURISRPC,
	ServeHTTP:   FindQuiddityByURIHTTP,
}

// FindQuiddityByURISRPC is sRPC handler of FindQuiddityByURI service.
func FindQuiddityByURISRPC(st protocol.Stream) {
	var req = &findQuiddityByURIReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *findQuiddityByURIRes
	res, err = findQuiddityByURI(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// FindQuiddityByURIHTTP is HTTP handler of FindQuiddityByURI service.
func FindQuiddityByURIHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &findQuiddityByURIReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *findQuiddityByURIRes
	res, err = findQuiddityByURI(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type findQuiddityByURIReq struct {
	URI    string
	Offset uint64
	Limit  uint64
}

type findQuiddityByURIRes struct {
	IDs [][32]byte `json:",string"`
}

func findQuiddityByURI(st protocol.Stream, req *findQuiddityByURIReq) (res *findQuiddityByURIRes, err protocol.Error) {
	var q = data.Quiddity{
		URI: req.URI,
	}
	var indexRes [][32]byte
	indexRes, err = q.FindIDsByURI(req.Offset, req.Limit)
	if err != nil {
		return
	}

	res = &findQuiddityByURIRes{
		IDs: indexRes,
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *findQuiddityByURIReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	req.URI = syllab.UnsafeGetString(buf, 0)
	req.Offset = syllab.GetUInt64(buf, 8)
	req.Limit = syllab.GetUInt64(buf, 16)
	return
}

func (req *findQuiddityByURIReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	heapIndex = syllab.SetString(buf, req.URI, 0, heapIndex)
	syllab.SetUInt64(buf, 8, req.Offset)
	syllab.SetUInt64(buf, 16, req.Limit)
	return
}

func (req *findQuiddityByURIReq) LenOfSyllabStack() uint32 {
	return 24
}

func (req *findQuiddityByURIReq) LenOfSyllabHeap() (ln uint32) {
	ln = uint32(len(req.URI))
	return
}

func (req *findQuiddityByURIReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *findQuiddityByURIReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "URI":
			req.URI, err = decoder.DecodeString()
		case "Offset":
			req.Offset, err = decoder.DecodeUInt64()
		case "Limit":
			req.Limit, err = decoder.DecodeUInt64()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *findQuiddityByURIReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"URI":"`)
	encoder.EncodeString(req.URI)
	encoder.EncodeString(`","Offset":`)
	encoder.EncodeUInt64(req.Offset)
	encoder.EncodeString(`,"Limit":`)
	encoder.EncodeUInt64(req.Limit)
	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *findQuiddityByURIReq) LenAsJSON() (ln int) {
	ln = len(req.URI)
	ln += 69
	return
}

/*
	Response Encoders & Decoders
*/

func (res *findQuiddityByURIRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	res.IDs = syllab.UnsafeGet32ByteArraySlice(buf, 128)
	return
}

func (res *findQuiddityByURIRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.Set32ByteArrayArray(buf, res.IDs, 0, heapIndex)
	return
}

func (res *findQuiddityByURIRes) LenOfSyllabStack() uint32 {
	return 8
}

func (res *findQuiddityByURIRes) LenOfSyllabHeap() (ln uint32) {
	ln = uint32(len(res.IDs) * 32)
	return
}

func (res *findQuiddityByURIRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *findQuiddityByURIRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "IDs":
			res.IDs, err = decoder.Decode32ByteArraySliceAsBase64()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (res *findQuiddityByURIRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"IDs":[`)
	encoder.Encode32ByteArraySliceAsBase64(res.IDs)

	encoder.EncodeString(`]}`)
}

func (res *findQuiddityByURIRes) LenAsJSON() (ln int) {
	ln = len(res.IDs) * 46
	ln += 8
	return
}
