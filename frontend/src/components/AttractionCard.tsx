// frontend/src/components/AttractionCard.tsx

interface AttractionProps {
    name: string;
    category: string;
}

export default function AttractionCard({ name, category }: AttractionProps) {
    return (
        <div className="border rounded-lg p-4 shadow-md bg-white">
            <h2 className="text-lg font-bold">{name}</h2>
            <p className="text-gray-600">Category: {category}</p>
        </div>
    );
}
