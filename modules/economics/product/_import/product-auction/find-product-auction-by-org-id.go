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

var findProductAuctionByOrgIDService = service.Service{
	URN:                "urn:giti:sabz.city:service:find-product-auction-by-org-id",
	Domain:             DomainName,
	ID:                 6120030510758381643,
	IssueDate:          1605376667,
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
			Name:        "Find Product Auction By Org ID",
			Description: "",
			TAGS:        []string{"ProductAuction"},
		},
	},

	SRPCHandler: FindProductAuctionByOrgIDSRPC,
	ServeHTTP:   FindProductAuctionByOrgIDHTTP,
}

// FindProductAuctionByOrgIDSRPC is sRPC handler of FindProductAuctionByOrgID service.
func FindProductAuctionByOrgIDSRPC(st protocol.Stream) {
	var req = &findProductAuctionByOrgIDReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *findProductAuctionByOrgIDRes
	res, err = findProductAuctionByOrgID(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// FindProductAuctionByOrgIDHTTP is HTTP handler of FindProductAuctionByOrgID service.
func FindProductAuctionByOrgIDHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &findProductAuctionByOrgIDReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *findProductAuctionByOrgIDRes
	res, err = findProductAuctionByOrgID(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type findProductAuctionByOrgIDReq struct {
	OrgID  [32]byte `json:",string"`
	Offset uint64
	Limit  uint64
}

type findProductAuctionByOrgIDRes struct {
	IDs [][32]byte `json:",string"`
}

func findProductAuctionByOrgID(st protocol.Stream, req *findProductAuctionByOrgIDReq) (res *findProductAuctionByOrgIDRes, err protocol.Error) {
	var pa = data.ProductAuction{
		OrgID: req.OrgID,
	}
	var indexRes [][32]byte
	indexRes, err = pa.FindIDsByOrgID(req.Offset, req.Limit)
	if err != nil {
		return
	}

	res = &findProductAuctionByOrgIDRes{
		IDs: indexRes,
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *findProductAuctionByOrgIDReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.OrgID[:], buf[0:])
	req.Offset = syllab.GetUInt64(buf, 32)
	req.Limit = syllab.GetUInt64(buf, 40)
	return
}

func (req *findProductAuctionByOrgIDReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.OrgID[:])
	syllab.SetUInt64(buf, 32, req.Offset)
	syllab.SetUInt64(buf, 40, req.Limit)
	return
}

func (req *findProductAuctionByOrgIDReq) LenOfSyllabStack() uint32 {
	return 48
}

func (req *findProductAuctionByOrgIDReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *findProductAuctionByOrgIDReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *findProductAuctionByOrgIDReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "OrgID":
			err = decoder.DecodeByteArrayAsBase64(req.OrgID[:])
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

func (req *findProductAuctionByOrgIDReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"OrgID":"`)
	encoder.EncodeByteSliceAsBase64(req.OrgID[:])

	encoder.EncodeString(`","Offset":`)
	encoder.EncodeUInt64(req.Offset)

	encoder.EncodeString(`,"Limit":`)
	encoder.EncodeUInt64(req.Limit)

	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *findProductAuctionByOrgIDReq) LenAsJSON() (ln int) {
	ln = 114
	return
}

/*
	Response Encoders & Decoders
*/

func (res *findProductAuctionByOrgIDRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	res.IDs = syllab.UnsafeGet32ByteArraySlice(buf, 128)
	return
}

func (res *findProductAuctionByOrgIDRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.Set32ByteArrayArray(buf, res.IDs, 0, heapIndex)
	return
}

func (res *findProductAuctionByOrgIDRes) LenOfSyllabStack() uint32 {
	return 8
}

func (res *findProductAuctionByOrgIDRes) LenOfSyllabHeap() (ln uint32) {
	ln = uint32(len(res.IDs) * 32)
	return
}

func (res *findProductAuctionByOrgIDRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *findProductAuctionByOrgIDRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
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

func (res *findProductAuctionByOrgIDRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"IDs":[`)
	encoder.Encode32ByteArraySliceAsBase64(res.IDs)

	encoder.EncodeString(`]}`)
}

func (res *findProductAuctionByOrgIDRes) LenAsJSON() (ln int) {
	ln = len(res.IDs) * 46
	ln += 8
	return
}
