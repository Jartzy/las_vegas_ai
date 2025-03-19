import React from 'react';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

/**
 * Props for the Map component
 * @interface MapProps
 */
interface MapProps {
  /** Latitude coordinate for the map center */
  latitude: number;
  /** Longitude coordinate for the map center */
  longitude: number;
  /** Zoom level for the map (default: 14) */
  zoom?: number;
  /** Array of markers to display on the map */
  markers?: Array<{
    /** Latitude coordinate for the marker */
    latitude: number;
    /** Longitude coordinate for the marker */
    longitude: number;
    /** Optional title for the marker tooltip */
    title?: string;
  }>;
}

/**
 * Map component that displays an interactive Google Map with optional markers
 * 
 * @component
 * @example
 * ```tsx
 * <Map
 *   latitude={36.1699}
 *   longitude={-115.1398}
 *   zoom={14}
 *   markers={[
 *     {
 *       latitude: 36.1699,
 *       longitude: -115.1398,
 *       title: "Event Location"
 *     }
 *   ]}
 * />
 * ```
 */
const Map: React.FC<MapProps> = ({ latitude, longitude, zoom = 14, markers = [] }) => {
  const mapStyles = {
    height: '100%',
    width: '100%',
  };

  const defaultCenter = {
    lat: latitude,
    lng: longitude,
  };

  return (
    <LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''}>
      <GoogleMap
        mapContainerStyle={mapStyles}
        zoom={zoom}
        center={defaultCenter}
        options={{
          zoomControl: true,
          streetViewControl: false,
          mapTypeControl: false,
          fullscreenControl: false,
        }}
      >
        {markers.map((marker, index) => (
          <Marker
            key={index}
            position={{
              lat: marker.latitude,
              lng: marker.longitude,
            }}
            title={marker.title}
          />
        ))}
      </GoogleMap>
    </LoadScript>
  );
};

export default Map; 