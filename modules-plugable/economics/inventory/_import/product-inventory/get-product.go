/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"time"

	"libgo/authorization"
	"libgo/http"
	"libgo/json"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
)

var getProductService = service.Service{
	URN:                "urn:giti:sabz.city:service:get-product",
	Domain:             DomainName,
	ID:                 2676404645150576807,
	IssueDate:          1608124902,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All, // UserTypeOwner
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Get Product",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"Product",
	},

	SRPCHandler: GetProductSRPC,
	ServeHTTP:   GetProductHTTP,
}

// GetProductSRPC is sRPC handler of GetProduct service.
func GetProductSRPC(st protocol.Stream) {
	var req = &getProductReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *getProductRes
	res, err = getProduct(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// GetProductHTTP is HTTP handler of GetProduct service.
func GetProductHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &getProductReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *getProductRes
	res, err = getProduct(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type getProductReq struct {
	RecordID [32]byte `json:",string"`
}

type getProductRes struct {
	WriteTime time.Time

	AppInstanceID    [32]byte `json:",string"`
	UserConnectionID [32]byte `json:",string"`
	OwnerID          [32]byte `json:",string"`
	QuiddityID       [32]byte `json:",string"`
	Amount           int64    // Number||Gram||Liter	last transaction
	Balance          int64    // Number||Gram||Liter	overall

	ReferenceID      [32]byte `json:",string"`
	DCID             [32]byte `json:",string"`
	ProductAuctionID [32]byte `json:",string"`
	SellerID         [32]byte `json:",string"`
	Status           data.ProductInventoryStatus
}

func getProduct(st protocol.Stream, req *getProductReq) (res *getProductRes, err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}

	var pi = data.ProductInventory{
		RecordID: req.RecordID,
	}
	err = pi.GetByRecordID()
	if err != nil {
		return
	}

	if st.Connection.UserID != pi.OwnerID || st.Connection.UserID != pi.DCID {
		err = authorization.ErrUserNotAllow
		return
	}

	res = &getProductRes{
		WriteTime: pi.WriteTime,

		AppInstanceID:    pi.AppInstanceID,
		UserConnectionID: pi.UserConnectionID,
		OwnerID:          pi.OwnerID,
		QuiddityID:       pi.QuiddityID,
		Amount:           pi.Amount,
		Balance:          pi.Balance,

		ReferenceID:      pi.ReferenceID,
		DCID:             pi.DCID,
		ProductAuctionID: pi.ProductAuctionID,
		SellerID:         pi.SellerID,
		Status:           pi.Status,
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *getProductReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.RecordID[:], buf[0:])
	return
}

func (req *getProductReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.RecordID[:])
	return
}

func (req *getProductReq) LenOfSyllabStack() uint32 {
	return 32
}

func (req *getProductReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *getProductReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *getProductReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "RecordID":
			err = decoder.DecodeByteArrayAsBase64(req.RecordID[:])
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *getProductReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"RecordID":"`)
	encoder.EncodeByteSliceAsBase64(req.RecordID[:])

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (req *getProductReq) LenAsJSON() (ln int) {
	ln = 58
	return
}

/*
	Response Encoders & Decoders
*/

func (res *getProductRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	res.WriteTime = time.Time(syllab.GetInt64(buf, 0))
	copy(res.AppInstanceID[:], buf[8:])
	copy(res.UserConnectionID[:], buf[40:])
	copy(res.OwnerID[:], buf[72:])
	copy(res.QuiddityID[:], buf[104:])
	res.Amount = syllab.GetInt64(buf, 136)
	res.Balance = syllab.GetInt64(buf, 144)

	copy(res.ReferenceID[:], buf[152:])
	copy(res.DCID[:], buf[184:])
	copy(res.ProductAuctionID[:], buf[216:])
	copy(res.SellerID[:], buf[248:])
	res.Status = data.ProductInventoryStatus(syllab.GetUInt8(buf, 280))
	return
}

func (res *getProductRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.SetInt64(buf, 0, int64(res.WriteTime))
	copy(buf[8:], res.AppInstanceID[:])
	copy(buf[40:], res.UserConnectionID[:])
	copy(buf[72:], res.OwnerID[:])
	copy(buf[104:], res.QuiddityID[:])
	syllab.SetInt64(buf, 136, res.Amount)
	syllab.SetInt64(buf, 144, res.Balance)

	copy(buf[152:], res.ReferenceID[:])
	copy(buf[184:], res.DCID[:])
	copy(buf[216:], res.ProductAuctionID[:])
	copy(buf[248:], res.SellerID[:])
	syllab.SetUInt8(buf, 280, uint8(res.Status))
	return
}

func (res *getProductRes) LenOfSyllabStack() uint32 {
	return 281
}

func (res *getProductRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *getProductRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *getProductRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
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
		case "OwnerID":
			err = decoder.DecodeByteArrayAsBase64(res.OwnerID[:])
		case "QuiddityID":
			err = decoder.DecodeByteArrayAsBase64(res.QuiddityID[:])
		case "Amount":
			res.Amount, err = decoder.DecodeInt64()
		case "Balance":
			res.Balance, err = decoder.DecodeInt64()
		case "ReferenceID":
			err = decoder.DecodeByteArrayAsBase64(res.ReferenceID[:])
		case "DCID":
			err = decoder.DecodeByteArrayAsBase64(res.DCID[:])
		case "ProductAuctionID":
			err = decoder.DecodeByteArrayAsBase64(res.ProductAuctionID[:])
		case "SellerID":
			err = decoder.DecodeByteArrayAsBase64(res.SellerID[:])
		case "Status":
			var num uint8
			num, err = decoder.DecodeUInt8()
			res.Status = data.ProductInventoryStatus(num)
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (res *getProductRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"WriteTime":`)
	encoder.EncodeInt64(int64(res.WriteTime))

	encoder.EncodeString(`,"AppInstanceID":"`)
	encoder.EncodeByteSliceAsBase64(res.AppInstanceID[:])

	encoder.EncodeString(`","UserConnectionID":"`)
	encoder.EncodeByteSliceAsBase64(res.UserConnectionID[:])

	encoder.EncodeString(`","OwnerID":"`)
	encoder.EncodeByteSliceAsBase64(res.OwnerID[:])

	encoder.EncodeString(`","QuiddityID":"`)
	encoder.EncodeByteSliceAsBase64(res.QuiddityID[:])

	encoder.EncodeString(`","Amount":`)
	encoder.EncodeInt64(res.Amount)

	encoder.EncodeString(`,"Balance":`)
	encoder.EncodeInt64(res.Balance)

	encoder.EncodeString(`,"ReferenceID":"`)
	encoder.EncodeByteSliceAsBase64(res.ReferenceID[:])

	encoder.EncodeString(`","DCID":"`)
	encoder.EncodeByteSliceAsBase64(res.DCID[:])

	encoder.EncodeString(`","ProductAuctionID":"`)
	encoder.EncodeByteSliceAsBase64(res.ProductAuctionID[:])

	encoder.EncodeString(`","SellerID":"`)
	encoder.EncodeByteSliceAsBase64(res.SellerID[:])

	encoder.EncodeString(`","Status":`)
	encoder.EncodeUInt8(uint8(res.Status))

	encoder.EncodeByte('}')
	return encoder.Buf
}

func (res *getProductRes) LenAsJSON() (ln int) {
	ln = 587
	return
}
