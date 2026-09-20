/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"libgo/achaemenid"
	"libgo/authorization"
	"libgo/ganjine"
	"libgo/http"
	"libgo/json"
	"libgo/math"
	"libgo/protocol"
	"libgo/service"
	"libgo/srpc"
	"libgo/syllab"
	"libgo/uuid"
	"libgo/validators"
)

var registerCustomProductAuctionService = service.Service{
	URN:                "urn:giti:sabz.city:service:register-custom-product-auction",
	Domain:             DomainName,
	ID:                 17158328769967041090,
	IssueDate:          1605189695,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDCreate,
		UserType: protocol.UserType_Org,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Register Custom Product Auction",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"ProductAuction",
	},

	SRPCHandler: RegisterCustomProductAuctionSRPC,
	ServeHTTP:   RegisterCustomProductAuctionHTTP,
}

// RegisterCustomProductAuctionSRPC is sRPC handler of RegisterCustomProductAuction service.
func RegisterCustomProductAuctionSRPC(st protocol.Stream) {
	var req = &registerCustomProductAuctionReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *registerCustomProductAuctionRes
	res, err = registerCustomProductAuction(st, req)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// RegisterCustomProductAuctionHTTP is HTTP handler of RegisterCustomProductAuction service.
func RegisterCustomProductAuctionHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &registerCustomProductAuctionReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *registerCustomProductAuctionRes
	res, err = registerCustomProductAuction(st, req)
	// Check if any error occur in business logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type registerCustomProductAuctionReq struct {
	ID [32]byte `json:",string"`

	// Price
	Discount                     math.PerMyriad
	DistributionCenterCommission math.PerMyriad
	SellerCommission             math.PerMyriad

	// Authorization
	Authorization authorization.Product

	Description string `valid:"text[0:50]"`
	Type        data.ProductAuctionType
}

type registerCustomProductAuctionRes struct {
	ID [32]byte `json:",string"`
}

func registerCustomProductAuction(st protocol.Stream, req *registerCustomProductAuctionReq) (res *registerCustomProductAuctionRes, err protocol.Error) {
	err = st.Authorize()
	if err != nil {
		return
	}

	// Validate data here due to service use internally by other services!
	err = req.validator()
	if err != nil {
		return
	}

	var pa = data.ProductAuction{
		ID: req.ID,
	}
	err = pa.GetLastByID()
	if err.Equal(ganjine.ErrRecordNotFound) {
		err = ErrProductAuctionDefaultNotRegistered
		return
	}
	if err != nil {
		return
	}
	if pa.OrgID != st.Connection.UserID {
		err = authorization.ErrUserNotAllow
		return
	}
	if pa.Status == data.QuiddityStatusBlocked {
		err = ErrBlockedByJustice
		return
	}

	pa = data.ProductAuction{
		AppInstanceID:    achaemenid.App.Nodes.LocalNode.InstanceID,
		UserConnectionID: st.Connection.ID,
		OrgID:            st.Connection.UserID,
		ID:               uuid.Random32Byte(),
		QuiddityID:       pa.QuiddityID,

		Discount:         req.Discount,
		DCCommission:     req.DistributionCenterCommission,
		SellerCommission: req.SellerCommission,

		// Authorization
		Authorization: req.Authorization,

		Description: req.Description,
		Type:        req.Type,
		Status:      data.ProductAuctionRegistered,
	}
	err = pa.SaveNew()
	if err != nil {
		return
	}

	res = &registerCustomProductAuctionRes{
		ID: pa.ID,
	}
	return
}

func (req *registerCustomProductAuctionReq) validator() (err protocol.Error) {
	err = validators.ValidateText(req.Description, 0, 50)
	return
}

/*
	Request Encoders & Decoders
*/

func (req *registerCustomProductAuctionReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.ID[:], buf[0:])

	req.Discount = math.PerMyriad(syllab.GetUInt16(buf, 32))
	req.DistributionCenterCommission = math.PerMyriad(syllab.GetUInt16(buf, 34))
	req.SellerCommission = math.PerMyriad(syllab.GetUInt16(buf, 36))

	req.Authorization.FromSyllab(buf, 38)

	req.Description = syllab.UnsafeGetString(buf, 38+req.Authorization.LenOfSyllabStack())
	req.Type = data.ProductAuctionType(syllab.GetUInt8(buf, 46+req.Authorization.LenOfSyllabStack()))
	return
}

func (req *registerCustomProductAuctionReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], req.ID[:])

	syllab.SetUInt16(buf, 32, uint16(req.Discount))
	syllab.SetUInt16(buf, 34, uint16(req.DistributionCenterCommission))
	syllab.SetUInt16(buf, 36, uint16(req.SellerCommission))

	req.Authorization.ToSyllab(buf, 38)

	heapIndex = syllab.SetString(buf, req.Description, 38+req.Authorization.LenOfSyllabStack(), heapIndex)
	syllab.SetUInt8(buf, 46+req.Authorization.LenOfSyllabStack(), uint8(req.Type))
	return
}

func (req *registerCustomProductAuctionReq) LenOfSyllabStack() uint32 {
	return 47 + req.Authorization.LenOfSyllabStack()
}

func (req *registerCustomProductAuctionReq) LenOfSyllabHeap() (ln uint32) {
	ln += req.Authorization.LenOfSyllabHeap()
	ln += uint32(len(req.Description))
	return
}

func (req *registerCustomProductAuctionReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *registerCustomProductAuctionReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "ID":
			err = decoder.DecodeByteArrayAsBase64(req.ID[:])

		case "Discount":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.Discount = math.PerMyriad(num)
		case "DistributionCenterCommission":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.DistributionCenterCommission = math.PerMyriad(num)
		case "SellerCommission":
			var num uint16
			num, err = decoder.DecodeUInt16()
			req.SellerCommission = math.PerMyriad(num)

		case "Authorization":
			err = req.Authorization.JSONDecoder(&decoder)

		case "Description":
			req.Description, err = decoder.DecodeString()
		case "Type":
			var num uint8
			num, err = decoder.DecodeUInt8()
			req.Type = data.ProductAuctionType(num)
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *registerCustomProductAuctionReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"ID":"`)
	encoder.EncodeByteSliceAsBase64(req.ID[:])

	encoder.EncodeString(`","Discount":`)
	encoder.EncodeUInt16(uint16(req.Discount))
	encoder.EncodeString(`,"DistributionCenterCommission":`)
	encoder.EncodeUInt16(uint16(req.DistributionCenterCommission))
	encoder.EncodeString(`,"SellerCommission":`)
	encoder.EncodeUInt16(uint16(req.SellerCommission))

	encoder.EncodeString(`,"Authorization":`)
	req.Authorization.JSONEncoder(&encoder)

	encoder.EncodeString(`,"Description":"`)
	encoder.EncodeString(req.Description)
	encoder.EncodeString(`","Type":`)
	encoder.EncodeUInt8(uint8(req.Type))

	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *registerCustomProductAuctionReq) LenAsJSON() (ln int) {
	ln = len(req.Description)
	ln += req.Authorization.LenAsJSON()
	ln += 179
	return
}

/*
	Response Encoders & Decoders
*/

func (res *registerCustomProductAuctionRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(res.ID[:], buf[0:])
	return
}

func (res *registerCustomProductAuctionRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[0:], res.ID[:])
	return
}

func (res *registerCustomProductAuctionRes) LenOfSyllabStack() uint32 {
	return 32
}

func (res *registerCustomProductAuctionRes) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *registerCustomProductAuctionRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *registerCustomProductAuctionRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "ID":
			err = decoder.DecodeByteArrayAsBase64(res.ID[:])
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (res *registerCustomProductAuctionRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"ID":"`)
	encoder.EncodeByteSliceAsBase64(res.ID[:])

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (res *registerCustomProductAuctionRes) LenAsJSON() (ln int) {
	ln = 52
	return
}
