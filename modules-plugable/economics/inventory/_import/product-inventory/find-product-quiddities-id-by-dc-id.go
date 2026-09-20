/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"libgo/authorization"
	"libgo/http"
	"libgo/json"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
)

var findProductQuidditiesIDByDCIDService = service.Service{
	URN:                "urn:giti:sabz.city:service:find-product-quiddities-id-by-dc-id",
	Domain:             DomainName,
	ID:                 9553492271168721174,
	IssueDate:          1612501864,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All ^ protocol.UserType_Unset,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Find Product Quiddities ID By DC ID",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"",
	},

	SRPCHandler: FindProductQuidditiesIDByDCIDSRPC,
	ServeHTTP:   FindProductQuidditiesIDByDCIDHTTP,
}

// FindProductQuidditiesIDByDCIDSRPC is sRPC handler of FindProductQuidditiesIDByDCID service.
func FindProductQuidditiesIDByDCIDSRPC(st protocol.Stream) {
	var req = &findProductQuidditiesIDByDCIDReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *findProductQuidditiesIDByDCIDRes
	res, err = findProductQuidditiesIDByDCID(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// FindProductQuidditiesIDByDCIDHTTP is HTTP handler of FindProductQuidditiesIDByDCID service.
func FindProductQuidditiesIDByDCIDHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &findProductQuidditiesIDByDCIDReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *findProductQuidditiesIDByDCIDRes
	res, err = findProductQuidditiesIDByDCID(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type findProductQuidditiesIDByDCIDReq struct {
	DCID   [32]byte `json:",string"`
	Offset uint64
	Limit  uint64
}

type findProductQuidditiesIDByDCIDRes struct {
	RecordIDs [][32]byte `json:",string"`
}

func findProductQuidditiesIDByDCID(st protocol.Stream, req *findProductQuidditiesIDByDCIDReq) (res *findProductQuidditiesIDByDCIDRes, err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}
	// TODO::: check other person access??
	var pi = data.ProductInventory{
		DCID: req.DCID,
	}
	var indexRes [][32]byte
	indexRes, err = pi.FindQuiddityIDsByDCID(req.Offset, req.Limit)
	if err != nil {
		return
	}

	res = &findProductQuidditiesIDByDCIDRes{
		RecordIDs: indexRes,
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *findProductQuidditiesIDByDCIDReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.DCID[:], buf[0:])
	req.Offset = syllab.GetUInt64(buf, 32)
	req.Limit = syllab.GetUInt64(buf, 40)
	return
}

func (req *findProductQuidditiesIDByDCIDReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.DCID[:])
	syllab.SetUInt64(buf, 32, req.Offset)
	syllab.SetUInt64(buf, 40, req.Limit)
	return
}

func (req *findProductQuidditiesIDByDCIDReq) LenOfSyllabStack() uint32 {
	return 48
}

func (req *findProductQuidditiesIDByDCIDReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *findProductQuidditiesIDByDCIDReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *findProductQuidditiesIDByDCIDReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "DCID":
			err = decoder.DecodeByteArrayAsBase64(req.DCID[:])
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

func (req *findProductQuidditiesIDByDCIDReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"DCID":"`)
	encoder.EncodeByteSliceAsBase64(req.DCID[:])
	encoder.EncodeString(`","Offset":`)
	encoder.EncodeUInt64(req.Offset)
	encoder.EncodeString(`,"Limit":`)
	encoder.EncodeUInt64(req.Limit)
	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *findProductQuidditiesIDByDCIDReq) LenAsJSON() (ln int) {
	ln = 113
	return
}

/*
	Response Encoders & Decoders
*/

func (res *findProductQuidditiesIDByDCIDRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	res.RecordIDs = syllab.UnsafeGet32ByteArraySlice(buf, 128)
	return
}

func (res *findProductQuidditiesIDByDCIDRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.Set32ByteArrayArray(buf, res.RecordIDs, 0, heapIndex)
	return
}

func (res *findProductQuidditiesIDByDCIDRes) LenOfSyllabStack() uint32 {
	return 8
}

func (res *findProductQuidditiesIDByDCIDRes) LenOfSyllabHeap() (ln uint32) {
	ln = uint32(len(res.RecordIDs) * 32)
	return
}

func (res *findProductQuidditiesIDByDCIDRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *findProductQuidditiesIDByDCIDRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
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

func (res *findProductQuidditiesIDByDCIDRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"RecordIDs":[`)
	encoder.Encode32ByteArraySliceAsBase64(res.RecordIDs)

	encoder.EncodeString(`]}`)
}

func (res *findProductQuidditiesIDByDCIDRes) LenAsJSON() (ln int) {
	ln = len(res.RecordIDs) * 46
	ln += 16
	return
}
