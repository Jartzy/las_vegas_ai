// frontend/src/components/AttractionCard.tsx
interface AttractionCardProps {
    name: string;
    category: string;
    description?: string;
    eventDate?: string;
    venue?: string;
}

export default function AttractionCard({
    name,
    category,
    description,
    eventDate,
    venue,
}: AttractionCardProps) {
    return (
        <div className="border p-4 rounded shadow">
            <h2 className="text-xl font-bold">{name}</h2>
            <p className="text-sm text-gray-600">{category}</p>
            {description && <p className="mt-2">{description}</p>}
            {eventDate && <p className="mt-1">Date: {new Date(eventDate).toLocaleString()}</p>}
            {venue && <p className="mt-1">Venue: {venue}</p>}
        </div>
    );
}