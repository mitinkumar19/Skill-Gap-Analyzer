import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, XCircle, Info, ChevronRight } from 'lucide-react';

const comparisonData = [
    {
        feature: "Accuracy",
        them: "60-70% (hallucinations common)",
        us: "95%+ (strict provenance)",
        themIcon: <XCircle className="text-destructive h-5 w-5" />,
        usIcon: <CheckCircle2 className="text-emerald-500 h-5 w-5" />,
        details: "Generic tools often infer skills that aren't there. We verify every skill against the actual text."
    },
    {
        feature: "Phantom Skills",
        them: "Inferred 'Cloud' from 'AWS'",
        us: "Only exact matches accepted",
        themIcon: <XCircle className="text-destructive h-5 w-5" />,
        usIcon: <CheckCircle2 className="text-emerald-500 h-5 w-5" />,
        details: "We don't assume. If it's not in the resume, it's not in the extraction."
    },
    {
        feature: "Speed",
        them: "15-30s (full LLM)",
        us: "3-5s (90% local)",
        themIcon: <XCircle className="text-destructive h-5 w-5" />,
        usIcon: <CheckCircle2 className="text-emerald-500 h-5 w-5" />,
        details: "By running NLP locally, we avoid massive API overhead and deliver results instantly."
    },
    {
        feature: "Privacy",
        them: "Data sent to external APIs",
        us: "Local-first processing",
        themIcon: <XCircle className="text-destructive h-5 w-5" />,
        usIcon: <CheckCircle2 className="text-emerald-500 h-5 w-5" />,
        details: "Your resume text stays on your machine during the high-intensity processing phase."
    },
    {
        feature: "Context Awareness",
        them: "Treats all text equally",
        us: "Section-aware extraction",
        themIcon: <XCircle className="text-destructive h-5 w-5" />,
        usIcon: <CheckCircle2 className="text-emerald-500 h-5 w-5" />,
        details: "We know the difference between a 'Skills' section and 'Projects', adjusting our logic accordingly."
    }
];

export const CompetitiveComparison: React.FC = () => {
    return (
        <div className="space-y-12">
            <div className="grid lg:grid-cols-2 gap-8 items-stretch">
                {/* Us Card */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-600/10 via-emerald-600/5 to-transparent border border-emerald-500/20 p-8 shadow-2xl shadow-emerald-500/10"
                >
                    <div className="flex justify-between items-center mb-8">
                        <h4 className="text-2xl font-bold gradient-text">Skill Gap Analyzer</h4>
                        <div className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-500 text-xs font-bold uppercase tracking-wider border border-emerald-500/30">
                            The Smart Way
                        </div>
                    </div>
                    <ul className="space-y-6">
                        {comparisonData.map((item, i) => (
                            <li key={i} className="group flex items-start gap-4">
                                <div className="p-1 rounded-full bg-emerald-500/20 mt-1">
                                    {item.usIcon}
                                </div>
                                <div>
                                    <span className="block font-semibold text-foreground">{item.feature}</span>
                                    <span className="text-emerald-400 font-medium">{item.us}</span>
                                    <p className="text-xs text-muted-foreground mt-1 opacity-100 lg:opacity-0 lg:group-hover:opacity-100 transition-opacity">
                                        {item.details}
                                    </p>
                                </div>
                            </li>
                        ))}
                    </ul>
                </motion.div>

                {/* Them Card */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    className="rounded-3xl bg-muted/30 border border-border p-8"
                >
                    <div className="flex justify-between items-center mb-8 opacity-60">
                        <h4 className="text-2xl font-bold text-muted-foreground">Generic AI Tools</h4>
                        <div className="px-3 py-1 rounded-full bg-destructive/10 text-destructive text-xs font-bold uppercase tracking-wider">
                            Outdated
                        </div>
                    </div>
                    <ul className="space-y-6 opacity-60">
                        {comparisonData.map((item, i) => (
                            <li key={i} className="flex items-start gap-4">
                                <div className="p-1 rounded-full bg-destructive/10 mt-1">
                                    {item.themIcon}
                                </div>
                                <div>
                                    <span className="block font-semibold text-muted-foreground">{item.feature}</span>
                                    <span className="text-destructive/80 line-through decoration-destructive/50">{item.them}</span>
                                </div>
                            </li>
                        ))}
                    </ul>
                </motion.div>
            </div>

            {/* Example Box */}
            <motion.div
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className="p-6 rounded-2xl bg-card border border-border shadow-soft overflow-hidden relative"
            >
                <div className="absolute top-0 right-0 p-4 opacity-10">
                    <Info size={48} />
                </div>
                <h5 className="font-bold mb-4 flex items-center gap-2">
                    <ChevronRight className="text-primary" /> Real-World Example
                </h5>
                <div className="grid md:grid-cols-3 gap-6">
                    <div>
                        <p className="text-xs font-bold uppercase text-muted-foreground mb-2 tracking-widest">Resume Line</p>
                        <div className="p-3 rounded-lg bg-muted text-sm italic border border-border">
                            "Deployed applications using AWS Lambda"
                        </div>
                    </div>
                    <div>
                        <p className="text-xs font-bold uppercase text-destructive mb-2 tracking-widest">Generic Tool</p>
                        <div className="p-3 rounded-lg bg-destructive/5 text-sm border border-destructive/20 text-destructive/80">
                            ❌ AWS, Lambda, Cloud Computing, Serverless, Python
                            <p className="text-[10px] mt-1 italic">(Wrong! Python not mentioned)</p>
                        </div>
                    </div>
                    <div>
                        <p className="text-xs font-bold uppercase text-emerald-500 mb-2 tracking-widest">Our Tool</p>
                        <div className="p-3 rounded-lg bg-emerald-500/5 text-sm border border-emerald-500/20 text-emerald-400 font-bold">
                            ✅ AWS, Lambda
                            <p className="text-[10px] mt-1 italic">(Correct! Only what's written)</p>
                        </div>
                    </div>
                </div>
            </motion.div>
        </div>
    );
};
