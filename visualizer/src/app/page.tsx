


import { Graph } from './graph';
import { data } from "~/lib/data"

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b text-black bg-white">
      <Graph data={data} />
    </main>
  );
}
