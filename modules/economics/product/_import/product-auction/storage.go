/* For license and copyright information please see the LEGAL file in the code repository */

package data

import (
	"golang.org/x/crypto/sha3"

	"libgo/authorization"
	etime "libgo/earth-time"
	"libgo/ganjine"
	"libgo/math"
	"libgo/pehrest"
	"libgo/syllab"
)

const (
	productAuctionStructureID uint64 = 2815138939176777099
)

var productAuctionStructure = ds.DataStructure{
	URN:             "urn:giti:sabz.city:data-structure:product-auction",
	ID:              2815138939176777099,
	IssueDate:       1599286551,
	ExpiryDate:      0,
	ExpireInFavorOf: "",
	Status:          protocol.Software_PreAlpha,
	Structure:       ProductAuction{},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Product Auction",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Store the product auction data",
	},
	TAGS: []string{
		"",
	},
}

// ProductAuction ---Read locale description in productAuctionStructure---
type ProductAuction struct {
	RequestID  [16]byte // user-request domain
	ID         [16]byte `index-hash:"RecordID"`
	OrgID      [16]byte `index-hash:"ID"` // Sell can be register just by producer organization
	QuiddityID [16]byte `index-hash:"ID,ID[pair,Authorization.AllowUserID],ID[pair,Authorization.GroupID]"`

	// Price
	Discount         math.PerMyriad // minus from product price

	// DCCommission     math.PerMyriad // Distribution-Center(Org)
	// SellerCommission math.PerMyriad

	// Authorization
	Authorization authorization.Product

	// Description string // User custom text to identify Product Auction easily by each other for org and other users.
	Type        ProductAuctionType
	Status      ProductAuctionStatus
}

// SaveNew method set some data and write entire ProductAuction record with all indexes!
func (pa *ProductAuction) SaveNew() (err protocol.Error) {
	err = pa.Set()
	if err != nil {
		return
	}

	pa.IndexRecordIDForID()
	pa.IndexIDForOrgID()
	pa.IndexIDForQuiddityID()
	if pa.Authorization.AllowUserID != [32]byte{} {
		pa.IndexIDForQuiddityIDAllowUserID()
		pa.IndexIDForAllowUserID()
	}
	if pa.Authorization.GroupID != [32]byte{} {
		pa.IndexIDForQuiddityIDGroupID()
		pa.IndexIDForGroupID()
	}
	return
}

// Set method set some data and write entire ProductAuction record!
func (pa *ProductAuction) Set() (err protocol.Error) {
	pa.RecordStructureID = productAuctionStructureID
	pa.RecordSize = pa.LenAsSyllab()
	pa.WriteTime = time.Now()
	pa.OwnerAppID = protocol.OS.AppManifest().AppUUID()

	var req = ganjine.SetRecordReq{
		Type:   ganjine.RequestTypeBroadcast,
		Record: pa.ToSyllab(),
	}
	pa.RecordID = sha3.Sum256(req.Record[32:])
	copy(req.Record[0:], pa.RecordID[:])

	err = gsdk.SetRecord(&req)
	if err != nil {
		// TODO::: Handle error situation
	}

	return
}

// GetByRecordID method read all existing record data by given RecordID!
func (pa *ProductAuction) GetByRecordID() (err protocol.Error) {
	var req = ganjine.GetRecordReq{
		RecordID:          pa.RecordID,
		RecordStructureID: productAuctionStructureID,
	}
	var res *ganjine.GetRecordRes
	res, err = gsdk.GetRecord(&req)
	if err != nil {
		return
	}

	err = pa.FromSyllab(res.Record)
	if err != nil {
		return
	}

	if pa.RecordStructureID != productAuctionStructureID {
		err = ganjine.ErrMisMatchedStructureID
	}
	return
}

// GetLastByID method find and read last version of record by given pa.ID
func (pa *ProductAuction) GetLastByID() (err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: pa.hashIDForRecordID(),
		Offset:   18446744073709551615,
		Limit:    1,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	if err != nil {
		return
	}

	pa.RecordID = indexRes.IndexValues[0]
	err = pa.GetByRecordID()
	if err.Equal(ganjine.ErrMisMatchedStructureID) {
		protocol.App.Log(log.WarnEvent(domainEnglish, "Platform collapsed!! HASH Collision Occurred on", productAuctionStructureID)
	}
	return
}

/*
	-- Search Methods --
*/

// FindRecordsIDsByID find RecordsIDs by given ID
func (pa *ProductAuction) FindRecordsIDsByID(offset, limit uint64) (RecordsIDs [][32]byte, err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: pa.hashIDForRecordID(),
		Offset:   offset,
		Limit:    limit,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	RecordsIDs = indexRes.IndexValues
	return
}

// FindIDsByOrgID find IDs by given OrgID
func (pa *ProductAuction) FindIDsByOrgID(offset, limit uint64) (IDs [][32]byte, err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: pa.hashOrgIDForID(),
		Offset:   offset,
		Limit:    limit,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	IDs = indexRes.IndexValues
	return
}

// FindIDsByQuiddityID find IDs by given QuiddityID
func (pa *ProductAuction) FindIDsByQuiddityID(offset, limit uint64) (IDs [][32]byte, err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: pa.hashQuiddityIDForID(),
		Offset:   offset,
		Limit:    limit,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	IDs = indexRes.IndexValues
	return
}

// FindIDsByQuiddityIDAllowUserID find IDs by given QuiddityID+AllowUserID
func (pa *ProductAuction) FindIDsByQuiddityIDAllowUserID(offset, limit uint64) (IDs [][32]byte, err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: pa.hashQuiddityIDAllowUserIDForID(),
		Offset:   offset,
		Limit:    limit,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	IDs = indexRes.IndexValues
	return
}

// FindIDsByQuiddityIDGroupID find IDs by given QuiddityID+GroupID
func (pa *ProductAuction) FindIDsByQuiddityIDGroupID(offset, limit uint64) (IDs [][32]byte, err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: pa.hashQuiddityIDGroupIDForID(),
		Offset:   offset,
		Limit:    limit,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	IDs = indexRes.IndexValues
	return
}

// FindIDsByAllowUserID find IDs by given AllowUserID
func (pa *ProductAuction) FindIDsByAllowUserID(offset, limit uint64) (IDs [][32]byte, err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: pa.hashAllowUserIDForID(),
		Offset:   offset,
		Limit:    limit,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	IDs = indexRes.IndexValues
	return
}

// FindIDsByGroupID find IDs by given GroupID
func (pa *ProductAuction) FindIDsByGroupID(offset, limit uint64) (IDs [][32]byte, err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: pa.hashGroupIDForID(),
		Offset:   offset,
		Limit:    limit,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	IDs = indexRes.IndexValues
	return
}

/*
	-- PRIMARY INDEXES --
*/

// IndexRecordIDForID save RecordID chain for ID
func (pa *ProductAuction) IndexRecordIDForID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pa.hashIDForRecordID(),
		IndexValue: pa.RecordID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pa *ProductAuction) hashIDForRecordID() (hash [32]byte) {
	const field = "ID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, productAuctionStructureID)
	copy(buf[8:], pa.ID[:])
	copy(buf[40:], field)
	return sha3.Sum256(buf)
}

/*
	-- SECONDARY INDEXES --
*/

// IndexIDForOrgID save ID chain for OrgID
func (pa *ProductAuction) IndexIDForOrgID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pa.hashOrgIDForID(),
		IndexValue: pa.ID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pa *ProductAuction) hashOrgIDForID() (hash [32]byte) {
	const field = "OrgID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, productAuctionStructureID)
	copy(buf[8:], pa.OrgID[:])
	copy(buf[40:], field)
	return sha3.Sum256(buf)
}

// IndexIDForQuiddityID save ID chain for QuiddityID
func (pa *ProductAuction) IndexIDForQuiddityID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pa.hashQuiddityIDForID(),
		IndexValue: pa.ID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pa *ProductAuction) hashQuiddityIDForID() (hash [32]byte) {
	const field = "QuiddityID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, productAuctionStructureID)
	copy(buf[8:], pa.QuiddityID[:])
	copy(buf[40:], field)
	return sha3.Sum256(buf)
}

// IndexIDForQuiddityIDAllowUserID save ID chain for QuiddityID+AllowUserID
func (pa *ProductAuction) IndexIDForQuiddityIDAllowUserID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pa.hashQuiddityIDAllowUserIDForID(),
		IndexValue: pa.ID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pa *ProductAuction) hashQuiddityIDAllowUserIDForID() (hash [32]byte) {
	const field = "QuiddityIDAllowUserID"
	var buf = make([]byte, 72+len(field)) // 8+32+32
	syllab.SetUInt64(buf, 0, productAuctionStructureID)
	copy(buf[8:], pa.QuiddityID[:])
	copy(buf[40:], pa.Authorization.AllowUserID[:])
	copy(buf[72:], field)
	return sha3.Sum256(buf)
}

// IndexIDForQuiddityIDGroupID save ID chain for QuiddityID+GroupID
func (pa *ProductAuction) IndexIDForQuiddityIDGroupID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pa.hashQuiddityIDGroupIDForID(),
		IndexValue: pa.ID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pa *ProductAuction) hashQuiddityIDGroupIDForID() (hash [32]byte) {
	const field = "QuiddityIDGroupID"
	var buf = make([]byte, 72+len(field)) // 8+32+32
	syllab.SetUInt64(buf, 0, productAuctionStructureID)
	copy(buf[8:], pa.QuiddityID[:])
	copy(buf[40:], pa.Authorization.GroupID[:])
	copy(buf[72:], field)
	return sha3.Sum256(buf)
}

// IndexIDForAllowUserID save ID chain for AllowUserID
func (pa *ProductAuction) IndexIDForAllowUserID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pa.hashAllowUserIDForID(),
		IndexValue: pa.ID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pa *ProductAuction) hashAllowUserIDForID() (hash [32]byte) {
	const field = "AllowUserID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, productAuctionStructureID)
	copy(buf[8:], pa.Authorization.AllowUserID[:])
	copy(buf[40:], field)
	return sha3.Sum256(buf)
}

// IndexIDForGroupID save ID chain for GroupID
func (pa *ProductAuction) IndexIDForGroupID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pa.hashGroupIDForID(),
		IndexValue: pa.ID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pa *ProductAuction) hashGroupIDForID() (hash [32]byte) {
	const field = "GroupID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, productAuctionStructureID)
	copy(buf[8:], pa.Authorization.GroupID[:])
	copy(buf[40:], field)
	return sha3.Sum256(buf)
}

/*
	-- Syllab Encoder & Decoder --
*/

func (pa *ProductAuction) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(payload)) < pa.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(pa.AppInstanceID[:], payload[88:])
	copy(pa.UserConnectionID[:], payload[120:])
	copy(pa.OrgID[:], payload[152:])
	copy(pa.ID[:], payload[184:])
	copy(pa.QuiddityID[:], payload[216:])

	pa.Discount = math.PerMyriad(syllab.GetUInt16(payload, 248))
	pa.DCCommission = math.PerMyriad(syllab.GetUInt16(payload, 250))
	pa.SellerCommission = math.PerMyriad(syllab.GetUInt16(payload, 252))

	pa.Authorization.FromSyllab(payload, 254)

	pa.Description = syllab.UnsafeGetString(payload, 254+pa.Authorization.LenOfSyllabStack())
	pa.Type = ProductAuctionType(syllab.GetUInt8(payload, 262+pa.Authorization.LenOfSyllabStack()))
	pa.Status = ProductAuctionStatus(syllab.GetUInt8(payload, 263+pa.Authorization.LenOfSyllabStack()))
}

func (pa *ProductAuction) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(payload[88:], pa.AppInstanceID[:])
	copy(payload[120:], pa.UserConnectionID[:])
	copy(payload[152:], pa.OrgID[:])
	copy(payload[184:], pa.ID[:])
	copy(payload[216:], pa.QuiddityID[:])

	syllab.SetUInt16(payload, 248, uint16(pa.Discount))
	syllab.SetUInt16(payload, 250, uint16(pa.DCCommission))
	syllab.SetUInt16(payload, 252, uint16(pa.SellerCommission))

	pa.Authorization.ToSyllab(payload, 254)

	heapIndex = syllab.SetString(payload, pa.Description, 254+pa.Authorization.LenOfSyllabStack(), heapIndex)
	syllab.SetUInt8(payload, 262+pa.Authorization.LenOfSyllabStack(), uint8(pa.Type))
	syllab.SetUInt8(payload, 263+pa.Authorization.LenOfSyllabStack(), uint8(pa.Status))
	return heapIndex
}

func (pa *ProductAuction) LenAsSyllab() uint64 {
	return uint64(pa.LenOfSyllabStack() + pa.LenOfSyllabHeap())
}
func (pa *ProductAuction) LenOfSyllabStack() uint32 { return 264 + pa.Authorization.LenOfSyllabStack() }
func (pa *ProductAuction) LenOfSyllabHeap() (ln uint32) {
	ln = pa.Authorization.LenOfSyllabHeap()
	ln += uint32(len(pa.Description))
	return
}

/*
	-- Record types --
*/

// ProductAuctionType indicate ProductAuction record type
// https://en.wikipedia.org/wiki/Auction_theory
type ProductAuctionType uint8

// ProductAuctionStatus indicate ProductAuction record status
type ProductAuctionStatus uint8

// ProductAuction status
const (
	ProductAuctionUnset ProductAuctionStatus = iota
	ProductAuctionRegistered
	ProductAuctionUpdated
	ProductAuctionExpired
	ProductAuctionBlocked
)
