/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"libgo/authorization"
	"libgo/http"
	"libgo/json"
	"libgo/protocol"
	"libgo/srpc"
	"libgo/syllab"
)

var findProductByQuiddityIDOwnerIDService = service.Service{
	URN:                "urn:giti:sabz.city:service:find-product-by-quiddity-id-owner-id",
	Domain:             DomainName,
	ID:                 3498679420775093054,
	IssueDate:          1610979719,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All,
	},

	Detail: map[protocol.LanguageID]service.ServiceDetail{
		protocol.LanguageEnglish: {
			Name:        "Find Product By Quiddity ID Owner ID",
			Description: "",
			TAGS:        []string{},
		},
	},

	SRPCHandler: FindProductByQuiddityIDOwnerIDSRPC,
	ServeHTTP:   FindProductByQuiddityIDOwnerIDHTTP,
}

// FindProductByQuiddityIDOwnerIDSRPC is sRPC handler of FindProductByQuiddityIDOwnerID service.
func FindProductByQuiddityIDOwnerIDSRPC(st protocol.Stream) {
	var req = &findProductByQuiddityIDOwnerIDReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *findProductByQuiddityIDOwnerIDRes
	res, err = findProductByQuiddityIDOwnerID(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// FindProductByQuiddityIDOwnerIDHTTP is HTTP handler of FindProductByQuiddityIDOwnerID service.
func FindProductByQuiddityIDOwnerIDHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &findProductByQuiddityIDOwnerIDReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *findProductByQuiddityIDOwnerIDRes
	res, err = findProductByQuiddityIDOwnerID(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type findProductByQuiddityIDOwnerIDReq struct {
	QuiddityID [32]byte `json:",string"`
	OwnerID    [32]byte `json:",string"`
	Offset     uint64
	Limit      uint64
}

type findProductByQuiddityIDOwnerIDRes struct {
	RecordIDs [][32]byte `json:",string"`
}

func findProductByQuiddityIDOwnerID(st protocol.Stream, req *findProductByQuiddityIDOwnerIDReq) (res *findProductByQuiddityIDOwnerIDRes, err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}
	var pi = data.ProductInventory{
		QuiddityID: req.QuiddityID,
		OwnerID:    req.OwnerID,
	}
	var indexRes [][32]byte
	indexRes, err = pi.FindRecordsIDsByQuiddityIDOwnerID(req.Offset, req.Limit)
	if err != nil {
		return
	}

	res = &findProductByQuiddityIDOwnerIDRes{
		RecordIDs: indexRes,
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *findProductByQuiddityIDOwnerIDReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.QuiddityID[:], buf[0:])
	copy(req.OwnerID[:], buf[32:])
	req.Offset = syllab.GetUInt64(buf, 64)
	req.Limit = syllab.GetUInt64(buf, 72)
	return
}

func (req *findProductByQuiddityIDOwnerIDReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.QuiddityID[:])
	copy(buf[32:], req.OwnerID[:])
	syllab.SetUInt64(buf, 64, req.Offset)
	syllab.SetUInt64(buf, 72, req.Limit)
	return
}

func (req *findProductByQuiddityIDOwnerIDReq) LenOfSyllabStack() uint32 {
	return 80
}

func (req *findProductByQuiddityIDOwnerIDReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *findProductByQuiddityIDOwnerIDReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *findProductByQuiddityIDOwnerIDReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "QuiddityID":
			err = decoder.DecodeByteArrayAsBase64(req.QuiddityID[:])
		case "OwnerID":
			err = decoder.DecodeByteArrayAsBase64(req.OwnerID[:])
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

func (req *findProductByQuiddityIDOwnerIDReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"QuiddityID":"`)
	encoder.EncodeByteSliceAsBase64(req.QuiddityID[:])

	encoder.EncodeString(`","OwnerID":"`)
	encoder.EncodeByteSliceAsBase64(req.OwnerID[:])

	encoder.EncodeString(`","Offset":`)
	encoder.EncodeUInt64(req.Offset)

	encoder.EncodeString(`,"Limit":`)
	encoder.EncodeUInt64(req.Limit)

	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *findProductByQuiddityIDOwnerIDReq) LenAsJSON() (ln int) {
	ln += 175
	return
}

/*
	Response Encoders & Decoders
*/

func (res *findProductByQuiddityIDOwnerIDRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	res.RecordIDs = syllab.UnsafeGet32ByteArraySlice(buf, 128)
	return
}

func (res *findProductByQuiddityIDOwnerIDRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.Set32ByteArrayArray(buf, res.RecordIDs, 0, heapIndex)
	return
}

func (res *findProductByQuiddityIDOwnerIDRes) LenOfSyllabStack() uint32 {
	return 8
}

func (res *findProductByQuiddityIDOwnerIDRes) LenOfSyllabHeap() (ln uint32) {
	ln = uint32(len(res.RecordIDs) * 32)
	return
}

func (res *findProductByQuiddityIDOwnerIDRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *findProductByQuiddityIDOwnerIDRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "RecordIDs":
			res.RecordIDs, err = decoder.Decode32ByteArraySliceAsBase64()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (res *findProductByQuiddityIDOwnerIDRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"RecordIDs":[`)
	encoder.Encode32ByteArraySliceAsBase64(res.RecordIDs)

	encoder.EncodeString(`]}`)
}

func (res *findProductByQuiddityIDOwnerIDRes) LenAsJSON() (ln int) {
	ln = len(res.RecordIDs) * 46
	ln += 16
	return
}
