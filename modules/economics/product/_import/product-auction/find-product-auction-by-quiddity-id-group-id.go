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

var findProductAuctionByQuiddityIDGroupIDService = service.Service{
	URN:                "urn:giti:sabz.city:service:find-product-auction-by-quiddity-id-group-id",
	Domain:             DomainName,
	ID:                 10222563312060962986,
	IssueDate:          1605202810,
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
			Name:        "Find Product Auction By Quiddity ID Group ID",
			Description: "",
			TAGS:        []string{"ProductAuction"},
		},
	},

	SRPCHandler: FindProductAuctionByQuiddityIDGroupIDSRPC,
	ServeHTTP:   FindProductAuctionByQuiddityIDGroupIDHTTP,
}

// FindProductAuctionByQuiddityIDGroupIDSRPC is sRPC handler of FindProductAuctionByQuiddityIDGroupID service.
func FindProductAuctionByQuiddityIDGroupIDSRPC(st protocol.Stream) {
	var req = &findProductAuctionByQuiddityIDGroupIDReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *findProductAuctionByQuiddityIDGroupIDRes
	res, err = findProductAuctionByQuiddityIDGroupID(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// FindProductAuctionByQuiddityIDGroupIDHTTP is HTTP handler of FindProductAuctionByQuiddityIDGroupID service.
func FindProductAuctionByQuiddityIDGroupIDHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &findProductAuctionByQuiddityIDGroupIDReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *findProductAuctionByQuiddityIDGroupIDRes
	res, err = findProductAuctionByQuiddityIDGroupID(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type findProductAuctionByQuiddityIDGroupIDReq struct {
	QuiddityID [32]byte `json:",string"`
	GroupID    [32]byte `json:",string"`
	Offset     uint64
	Limit      uint64
}

type findProductAuctionByQuiddityIDGroupIDRes struct {
	IDs [][32]byte `json:",string"`
}

func findProductAuctionByQuiddityIDGroupID(st protocol.Stream, req *findProductAuctionByQuiddityIDGroupIDReq) (res *findProductAuctionByQuiddityIDGroupIDRes, err protocol.Error) {
	var pa = data.ProductAuction{
		QuiddityID: req.QuiddityID,
		Authorization: authorization.Product{
			GroupID: req.GroupID,
		},
	}
	var indexRes [][32]byte
	indexRes, err = pa.FindIDsByQuiddityIDGroupID(req.Offset, req.Limit)
	if err != nil {
		return
	}

	res = &findProductAuctionByQuiddityIDGroupIDRes{
		IDs: indexRes,
	}
	return
}

func (req *findProductAuctionByQuiddityIDGroupIDReq) validator() (err protocol.Error) {
	return
}

/*
	Request Encoders & Decoders
*/

func (req *findProductAuctionByQuiddityIDGroupIDReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.QuiddityID[:], buf[0:])
	copy(req.GroupID[:], buf[32:])
	req.Offset = syllab.GetUInt64(buf, 64)
	req.Limit = syllab.GetUInt64(buf, 72)
	return
}

func (req *findProductAuctionByQuiddityIDGroupIDReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.QuiddityID[:])
	copy(buf[32:], req.GroupID[:])
	syllab.SetUInt64(buf, 64, req.Offset)
	syllab.SetUInt64(buf, 72, req.Limit)
	return
}

func (req *findProductAuctionByQuiddityIDGroupIDReq) LenOfSyllabStack() uint32 {
	return 80
}

func (req *findProductAuctionByQuiddityIDGroupIDReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *findProductAuctionByQuiddityIDGroupIDReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *findProductAuctionByQuiddityIDGroupIDReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "QuiddityID":
			err = decoder.DecodeByteArrayAsBase64(req.QuiddityID[:])
		case "GroupID":
			err = decoder.DecodeByteArrayAsBase64(req.GroupID[:])
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

func (req *findProductAuctionByQuiddityIDGroupIDReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"QuiddityID":"`)
	encoder.EncodeByteSliceAsBase64(req.QuiddityID[:])

	encoder.EncodeString(`","GroupID":"`)
	encoder.EncodeByteSliceAsBase64(req.GroupID[:])

	encoder.EncodeString(`","Offset":`)
	encoder.EncodeUInt64(req.Offset)

	encoder.EncodeString(`,"Limit":`)
	encoder.EncodeUInt64(req.Limit)

	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *findProductAuctionByQuiddityIDGroupIDReq) LenAsJSON() (ln int) {
	ln = 171
	return
}

/*
	Response Encoders & Decoders
*/

func (res *findProductAuctionByQuiddityIDGroupIDRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	res.IDs = syllab.UnsafeGet32ByteArraySlice(buf, 128)
	return
}

func (res *findProductAuctionByQuiddityIDGroupIDRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.Set32ByteArrayArray(buf, res.IDs, 0, heapIndex)
	return
}

func (res *findProductAuctionByQuiddityIDGroupIDRes) LenOfSyllabStack() uint32 {
	return 8
}

func (res *findProductAuctionByQuiddityIDGroupIDRes) LenOfSyllabHeap() (ln uint32) {
	ln = uint32(len(res.IDs) * 32)
	return
}

func (res *findProductAuctionByQuiddityIDGroupIDRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *findProductAuctionByQuiddityIDGroupIDRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
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

func (res *findProductAuctionByQuiddityIDGroupIDRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"IDs":[`)
	encoder.Encode32ByteArraySliceAsBase64(res.IDs)

	encoder.EncodeString(`]}`)
}

func (res *findProductAuctionByQuiddityIDGroupIDRes) LenAsJSON() (ln int) {
	ln = len(res.IDs) * 46
	ln += 8
	return
}
